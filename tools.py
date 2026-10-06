"""The tools the harness can run, and the JSON that describes them to the model."""

import json
import re
import subprocess
import time
from datetime import date, datetime, timedelta
from functools import lru_cache
from pathlib import Path

import requests

# Open-Meteo is free and needs no API key. Its geocoder finds cities; Nominatim finds
# specific places (museums, parks) and needs a User-Agent that identifies the app.
CITY_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "climate-aware-itinerary-class-project/0.1"}

# The public OSRM demo server answers every profile with driving times, so walking
# goes to the OpenStreetMap foot-routing server instead.
ROUTE_URLS = {
    "driving": "https://router.project-osrm.org/route/v1/driving",
    "walking": "https://routing.openstreetmap.de/routed-foot/route/v1/driving",
}

ITINERARY_DIR = Path(__file__).parent / "Example Itineraries"
CONTEXT_FILE = Path(__file__).parent / "context.md"  # summary of ITINERARY_DIR, see build_context.py

# Open-Meteo's archive lags real time by a few days.
ARCHIVE_LAG_DAYS = 7
MAX_WEATHER_DAYS = 16
RAINY_DAY_INCHES = 0.5  # ~13 mm: more than a drizzle
WALKING_LIMIT_MIN = 20  # a longer walk than this, suggest driving or transit
OUTDOOR_HIGH_F = (50, 90)  # outside this range a day counts as too cold or too hot


def _error(message: str) -> str:
    # The model cannot see an exception. Return something it can reason about.
    return json.dumps({"error": message})


def geocode_place(name: str, country: str | None = None) -> str:
    """Resolve a city name to several candidates so the model can pick the right one."""
    params = {"name": name, "count": 5}
    if country:
        # The API only filters by two-letter code, so ask for more and match on name too.
        params["count"] = 10
    try:
        results = requests.get(CITY_GEOCODE_URL, params=params, timeout=10).json().get("results", [])
    except requests.RequestException as e:
        return _error(f"Geocoding service failed: {e}")

    if country:
        wanted = country.strip().lower()
        results = [r for r in results if wanted in (r.get("country", "").lower(), r.get("country_code", "").lower())]
    if not results:
        return _error(f"No city named '{name}'" + (f" in '{country}'" if country else "") + " was found.")

    return json.dumps({
        "candidates": [
            {
                "name": r["name"],
                "region": r.get("admin1"),
                "country": r.get("country"),
                "latitude": r["latitude"],
                "longitude": r["longitude"],
                "population": r.get("population"),
            }
            for r in results[:5]
        ]
    })


def _years_ago(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year - years)
    except ValueError:  # Feb 29 in a non-leap year
        return d.replace(year=d.year - years, day=28)


def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str) -> str:
    """Daily temperatures and precipitation for a date range in a past year."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return _error("Dates must be formatted YYYY-MM-DD.")
    if end < start:
        return _error("end_date is before start_date.")
    if (end - start).days + 1 > MAX_WEATHER_DAYS:
        return _error(f"Date range is too long. Ask for at most {MAX_WEATHER_DAYS} days.")

    # Trip dates are usually in the future. Slide the range back whole years until the
    # archive has it, so the model never has to do the year arithmetic.
    latest = date.today() - timedelta(days=ARCHIVE_LAG_DAYS)
    years_back = 0
    while _years_ago(end, years_back) > latest:
        years_back += 1
    start, end = _years_ago(start, years_back), _years_ago(end, years_back)
    start_date, end_date = start.isoformat(), end.isoformat()

    try:
        response = requests.get(
            ARCHIVE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "temperature_unit": "fahrenheit",
                "precipitation_unit": "inch",
                "timezone": "auto",
            },
            timeout=15,
        )
        daily = response.json()["daily"]
    except (requests.RequestException, KeyError, ValueError) as e:
        return _error(f"Weather service failed: {e}")

    days = [
        {
            "date": d,
            "high_f": hi,
            "low_f": lo,
            "precip_in": p,
            # Decided here, not by the model, so every day is judged by the same rule.
            "outdoor_ok": (p or 0) < RAINY_DAY_INCHES and OUTDOOR_HIGH_F[0] <= hi <= OUTDOOR_HIGH_F[1],
        }
        for d, hi, lo, p in zip(
            daily["time"], daily["temperature_2m_max"], daily["temperature_2m_min"], daily["precipitation_sum"]
        )
        if hi is not None
    ]
    if not days:
        return _error("No weather data came back for that location and range.")

    return json.dumps({
        # Grid-based data: typical conditions for the area, not an exact forecast.
        "note": "Past-year conditions from a coarse grid. Treat as typical, not exact.",
        "dates_queried": f"{start_date} to {end_date}",
        "days": days,
        "avg_high_f": round(sum(d["high_f"] for d in days) / len(days), 1),
        "avg_low_f": round(sum(d["low_f"] for d in days) / len(days), 1),
        "rainy_days": sum(1 for d in days if (d["precip_in"] or 0) >= RAINY_DAY_INCHES),
    })


def _strip_links(text: str) -> str:
    """[label](url) -> label. The URLs cost tokens and tell the model nothing about preferences."""
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)


def _read_text(path: Path) -> str:
    """File text. Some notes are RTF saved with a .md extension; macOS textutil converts those."""
    raw = path.read_text()
    if raw.startswith("{\\rtf"):
        return subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", str(path)], capture_output=True, text=True, check=True
        ).stdout
    return raw


def load_itineraries() -> list[dict]:
    """Every past itinerary and note as {trip, text}, with links stripped and blank lines removed."""
    return [
        {
            "trip": path.stem,
            "text": "\n".join(line.rstrip() for line in _strip_links(_read_text(path)).splitlines() if line.strip()),
        }
        for path in sorted(ITINERARY_DIR.rglob("*.md"))
    ]


def _context_is_fresh() -> bool:
    """True if context.md exists and no itinerary has changed since it was built."""
    if not CONTEXT_FILE.is_file():
        return False
    newest = max((p.stat().st_mtime for p in ITINERARY_DIR.rglob("*.md")), default=0)
    return CONTEXT_FILE.stat().st_mtime >= newest


def read_my_itineraries(keyword: str | None = None, preferences: str | None = None) -> str:
    """Return the user's travel-style summary, or the raw itineraries matching a keyword.

    If the user typed their own preferences in the UI, those win. Otherwise, without a keyword
    this returns context.md (built by build_context.py). With a keyword, or when context.md is
    missing or older than the itineraries, it reads the raw files.
    """
    if preferences and preferences.strip():
        return json.dumps({"summary": preferences.strip()})

    if not ITINERARY_DIR.is_dir():
        return _error("The Example Itineraries folder was not found.")

    if not keyword and _context_is_fresh():
        return json.dumps({"summary": CONTEXT_FILE.read_text()})

    itineraries = [
        trip for trip in load_itineraries() if not keyword or keyword.lower() in trip["text"].lower()
    ]

    if not itineraries:
        return _error(f"No past itineraries mention '{keyword}'. Call again without a keyword.")
    return json.dumps({"itineraries": itineraries})


@lru_cache(maxsize=256)
def _geocode_stop(query: str) -> tuple[float, float] | None:
    """Find one specific place with Nominatim. Cached, because its policy is 1 request/second."""
    time.sleep(1.1)
    results = requests.get(
        NOMINATIM_URL, params={"q": query, "format": "jsonv2", "limit": 1}, headers=HEADERS, timeout=10
    ).json()
    return (float(results[0]["lat"]), float(results[0]["lon"])) if results else None


def _route(mode: str, a: tuple[float, float], b: tuple[float, float]) -> dict | None:
    """One routed leg as {minutes, km}, or None if the router finds no route."""
    route = requests.get(
        f"{ROUTE_URLS[mode]}/{a[1]},{a[0]};{b[1]},{b[0]}", params={"overview": "false"}, timeout=15
    ).json()
    if route.get("code") != "Ok":
        return None
    leg = route["routes"][0]
    return {"minutes": round(leg["duration"] / 60), "km": round(leg["distance"] / 1000, 1)}


def get_travel_time(origin: str, destination: str, mode: str | None = None) -> str:
    """Geocode two places and route between them. Doubles as a check that both places exist."""
    if mode is not None and mode not in ROUTE_URLS:
        return _error(f"Unknown mode '{mode}'. Use one of {list(ROUTE_URLS)}, or omit it for both.")

    try:
        points = []
        for label, query in (("origin", origin), ("destination", destination)):
            point = _geocode_stop(query)
            if point is None:
                return _error(
                    f"Could not find {label} '{query}'. Retry with a different spelling "
                    "or add the city, or drop this place from the plan."
                )
            points.append(point)
        legs = {m: _route(m, *points) for m in ([mode] if mode else ROUTE_URLS)}
    except (requests.RequestException, ValueError) as e:
        return _error(f"Travel-time service failed: {e}")

    if not any(legs.values()):
        return _error(f"No route between '{origin}' and '{destination}'.")
    result = {"origin": origin, "destination": destination, **{m: leg for m, leg in legs.items() if leg}}
    if legs.get("walking") and legs.get("driving"):
        # Decided here so the plan never sends someone on an hour-long walk.
        result["suggested_mode"] = "walking" if legs["walking"]["minutes"] <= WALKING_LIMIT_MIN else "driving"
    return json.dumps(result)


# What the model sees: the "set notes" in the screenplay.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "geocode_place",
            "description": (
                "Look up a city and return up to 5 candidates with region, country, and "
                "latitude/longitude. Call this first to get coordinates for the weather tool. "
                "Names are ambiguous (Paris, France vs Paris, Texas), so pass country when the "
                "user gave one, and pick the most plausible candidate."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "City name, e.g. 'Lisbon'"},
                    "country": {"type": "string", "description": "Optional country name or 2-letter code, e.g. 'Portugal' or 'PT'"},
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_historical_weather",
            "description": (
                "Daily high/low temperature (F), precipitation (inches), and an outdoor_ok flag for a "
                "location over a date range. Pass the trip dates as given: if they are not far enough in the "
                "past for the archive, the tool uses the same dates from an earlier year to estimate "
                "typical conditions, and reports the dates it used. Days come back in trip order."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                    "start_date": {"type": "string", "description": "YYYY-MM-DD, first day of the trip"},
                    "end_date": {"type": "string", "description": "YYYY-MM-DD, last day of the trip"},
                },
                "required": ["latitude", "longitude", "start_date", "end_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_my_itineraries",
            "description": (
                "Returns a summary of the user's travel style (pacing, activity mix, tastes). Use to "
                "infer how to pace and fill the days. Call with no keyword first."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Optional. Returns the raw past itineraries mentioning it, e.g. 'beach' or 'museum'",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_travel_time",
            "description": (
                "Geocodes two places and returns walking and driving time (minutes, km) between them, "
                "plus a suggested_mode. Include the city in each name (e.g. 'Louvre Museum, Paris'). "
                "Returns an error if a place cannot be found, which means it may not exist: "
                "retry with another spelling, or drop or replace it."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "e.g. 'Louvre Museum, Paris'"},
                    "destination": {"type": "string", "description": "e.g. 'Eiffel Tower, Paris'"},
                    "mode": {"type": "string", "enum": ["walking", "driving"], "description": "Optional. Omit to get both."},
                },
                "required": ["origin", "destination"],
            },
        },
    },
]

# What the harness runs: tool name -> Python function.
TOOL_MAP = {
    "geocode_place": geocode_place,
    "get_historical_weather": get_historical_weather,
    "read_my_itineraries": read_my_itineraries,
    "get_travel_time": get_travel_time,
}


def run_tool(name: str, args: dict, preferences: str | None = None) -> str:
    """Run one tool call. Models invent tool names and arguments; never let that crash the loop.

    preferences is the user's own travel-style text from the UI. It comes from the harness,
    not the model, so the model cannot drop or rewrite it.
    """
    if name not in TOOL_MAP:
        return json.dumps({"error": f"Unknown tool '{name}'. Available: {list(TOOL_MAP)}"})
    if name == "read_my_itineraries":
        args = {**args, "preferences": preferences}
    try:
        return TOOL_MAP[name](**args)
    except TypeError as e:
        return json.dumps({"error": f"Bad arguments for {name}: {e}"})
