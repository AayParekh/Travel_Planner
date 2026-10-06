"""Distill the example itineraries into context.md, so the agent reads a short summary
instead of every raw itinerary. Run once, and again after adding or editing a trip:

    uv run build_context.py
"""

import litellm

from tools import CONTEXT_FILE, ITINERARY_DIR, load_itineraries

PROMPT = """Below are one traveler's past trip itineraries. Write a compact travel-style profile \
(750-1000 words, markdown) that a trip-planning agent will read instead of the originals:

- Pacing: typical stops per day, and how the day is split (morning/afternoon/evening).
- Activity mix: outdoor vs indoor vs food, with rough proportions. Also energy: if/how the days balance high-energy activities (hikes, day trips) with low-activity ones (parks, beaches). 
- Travel: how far they are willing to go between stops, and walking vs driving habits.å
- Tastes: recurring kinds of places and anything they clearly like or avoid.
- Two or three short example days, copied closely, as pacing references.

Only state things the itineraries support. Also take into account the reflections written in `General Guidelines.md`.

{itineraries}"""


def build() -> None:
    itineraries = load_itineraries()
    if not itineraries:
        raise SystemExit(f"No .md itineraries found in {ITINERARY_DIR}")

    text = "\n\n".join(f"## {trip['trip']}\n{trip['text']}" for trip in itineraries)
    reply = litellm.completion(
        model="vertex_ai/gemini-3.5-flash-lite",
        vertex_location="global",
        messages=[{"role": "user", "content": PROMPT.format(itineraries=text)}],
    ).choices[0].message.content

    CONTEXT_FILE.write_text(reply.strip() + "\n")
    print(f"Wrote {CONTEXT_FILE.name} from {len(itineraries)} itineraries ({len(reply.split())} words).")


if __name__ == "__main__":
    build()
