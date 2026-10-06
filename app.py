import json
import re
import uuid
from datetime import date
from pathlib import Path

import litellm
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from tools import TOOLS, run_tool

# --- Config ---

SYSTEM_PROMPT = """You are a climate-aware trip planner. Given a city, start date, and trip length \
(1 city, 1-7 days max), you GENERATE a day-by-day itinerary. Today is {today}.

If the city, start date, or number of days is missing, reply with a short question asking for \
it and call NO tools until you have all three. Never invent dates. If the user \
gives no year, use the next occurrence of those dates after today.

Work in this order:
1. geocode_place to resolve the city. If the name is ambiguous and the user gave no country, \
pick the most famous candidate and say which one you chose.
2. get_historical_weather with the trip dates (YYYY-MM-DD). The tool swaps in an earlier \
year when the archive needs it; do not adjust the year yourself.
3. read_my_itineraries to learn the user's pacing (stops per day), activity mix, and tastes.
4. Suggest places from your own knowledge. A day with outdoor_ok true gets outdoor activities \
(parks, viewpoints, walks, markets, temples and gardens); a day with outdoor_ok false gets \
indoor ones (museums, food halls, cafes, covered arcades). Every stop on an outdoor day must \
be outdoors and every stop on an indoor day indoors. Each day has 3 to 7 stops, each a real \
attraction, restaurant, or neighborhood, never a transit station. Pick the number per day from the \
user's pacing: fewer stops for long activities, long hops between stops, or after a heavy day; more \
for short activities that sit close together. Spread the stops across morning, afternoon, and \
evening. Group each day's stops by area.
5. Fix the order of each day's stops, then call get_travel_time for every consecutive pair of stops within the same day, in \
that final order (never between the last stop of one day and the first of the next), without a mode, and use its suggested_mode. It also verifies the place \
exists. If it reports a place not found, retry once with another spelling; if that fails, \
replace the place and check the new hop. Never list a place that failed the check. A place the \
user asks for goes through the same check; do not judge whether it exists from memory.

Final answer format, nothing else. Only quote a travel time that get_travel_time returned for \
that exact pair and its suggested_mode (use that mode's minutes, and write "walk" or "drive"; never write the words "suggested_mode"); the first stop of each day, including Day 2 onward, has no travel time and no mention of the previous day.
Day N (Month D) - Outdoor day or Indoor day: H/L F, rain X in, in one line; no year. Copy the label, temperatures and rain from that day's get_historical_weather entry: Outdoor day only if outdoor_ok is true, Indoor day if false. Write the real precip_in number for X (0 in if dry), never the word 'rain' alone.
- Morning: place(s), one short reason (X min walk, or X min drive, from previous stop; for the day's first stop, just the reason, no travel time)
- Afternoon: place(s), one short reason (X min walk, or X min drive, from previous stop)
- Evening: place(s), one short reason (X min walk, or X min drive, from previous stop)
List every stop of a part of the day on its own line, each with its own travel time, so the \
number of lines per day matches the number of stops.
Close with 2-3 lines on how weather and the user's past trips shaped the plan (cite only \
preferences you saw in them), and note that weather is typical conditions, not a forecast."""
MAX_TOOL_ROUNDS = 70  # geocode + weather + history + a travel time per hop (up to 6 per day, 7 days)

# --- The Harness ---


TRAVEL_NOTE = re.compile(r"\s*[,;:-]?\s*\(\s*(?:about\s*)?\d+\s*(?:min|minute)s?\b[^)]*\)", re.I)


def strip_first_stop_travel(text: str) -> str:
    """Remove the travel time from the first stop of each day: nothing precedes it.

    The prompt asks for this, but the model sometimes still writes "(11 min drive from previous
    stop)" on a day's first line, so enforce it here. Only the first bullet after each "Day N"
    heading is touched.
    """
    out, first = [], False
    for line in text.split("\n"):
        if re.match(r"\s*Day \d+", line):
            first = True
        elif first and line.lstrip().startswith("-"):
            line = TRAVEL_NOTE.sub("", line).rstrip()
            first = False
        out.append(line)
    return "\n".join(out)


def run_agent(messages: list[dict], preferences: str | None = None) -> tuple[str, list[dict]]:
    """Complete until the model answers without asking for a tool.

    Returns the final text and a record of every tool call made along the way.
    """
    tool_calls = []
    for kind, value in run_agent_events(messages, preferences):
        if kind == "tool_call":
            tool_calls += [value]
        else:
            return value, tool_calls


def run_agent_events(messages: list[dict], preferences: str | None = None):
    """The agent loop as a generator: yields ("tool_call", {...}) as each tool finishes,
    then ("done", final_text). Lets the UI show tool calls while the agent is still working.
    """
    for _ in range(MAX_TOOL_ROUNDS):
        reply = litellm.completion(
            model="vertex_ai/gemini-3.5-flash-lite",
            vertex_location="global",
            messages=messages,
            tools=TOOLS,
        ).choices[0].message

        # Append assistant's reply (text, tool calls, or both) to the context.
        # model_dump() keeps it a plain dict: the raw object carries provider-specific
        # fields that trip Pydantic when LiteLLM re-serializes it next round.
        messages += [reply.model_dump()]

        if not reply.tool_calls:
            yield "done", strip_first_stop_travel(reply.content or "")
            return

        # The harness, not the model, runs each tool and appends the result
        for call in reply.tool_calls:
            args = json.loads(call.function.arguments)
            result = run_tool(call.function.name, args, preferences)
            yield "tool_call", {"name": call.function.name, "args": args, "result": result}

            messages += [{"role": "tool", "tool_call_id": call.id, "content": result}]

    yield "done", "Sorry, I hit my tool-call limit before finishing."


# --- Session Store ---

# session_id -> list of messages. In-memory, single process.
sessions: dict[str, list] = {}

# --- FastAPI App ---

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    preferences: str | None = None  # user's own travel style; blank means use context.md


class ChatResponse(BaseModel):
    response: str
    session_id: str
    tool_calls: list[dict]


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/context")
def context():
    """The default preferences, shown pre-filled in the UI."""
    file = Path(__file__).parent / "context.md"
    return {"context": file.read_text() if file.is_file() else ""}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Get or create the session
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT.format(today=date.today().isoformat())}]

    # Append user's message to the context
    sessions[session_id] += [{"role": "user", "content": request.message}]

    try:
        response, tool_calls = run_agent(sessions[session_id], request.preferences)
    except Exception as e:
        # Auth, billing, a model that is not running: show it in the chat, not as a 500.
        response, tool_calls = f"Model call failed: {type(e).__name__}: {str(e)[:300]}", []

    return ChatResponse(response=response, session_id=session_id, tool_calls=tool_calls)


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    """Same as /chat, but streams newline-delimited JSON so the UI can show tool calls live.

    Events: {"type": "tool_call", "name", "args", "result"} as each tool finishes, then one
    {"type": "done", "response", "session_id", "tool_calls"} (the /chat response shape).
    """
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT.format(today=date.today().isoformat())}]
    sessions[session_id] += [{"role": "user", "content": request.message}]

    def events():
        tool_calls = []
        try:
            for kind, value in run_agent_events(sessions[session_id], request.preferences):
                if kind == "tool_call":
                    tool_calls += [value]
                    yield json.dumps({"type": "tool_call", **value}) + "\n"
                else:
                    response = value
        except Exception as e:
            response = f"Model call failed: {type(e).__name__}: {str(e)[:300]}"
        done = {"type": "done", "response": response, "session_id": session_id, "tool_calls": tool_calls}
        yield json.dumps(done) + "\n"

    return StreamingResponse(events(), media_type="application/x-ndjson")


@app.post("/clear")
def clear(session_id: str | None = None):
    sessions.pop(session_id, None)
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
