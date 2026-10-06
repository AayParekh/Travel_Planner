# Climate-Aware Itinerary Generator

An agentic trip planner (Agentic AI class project) on top of `gemini-web-tool-calling`.
Give it a city, start date, and trip length (3-4 days) and it generates a day-by-day
itinerary: outdoor activities on good-weather days, indoor ones on bad days, with stops
grouped so travel between them is short and paced like your past trips.

- The harness loop is `run_agent()` in `app.py`; the session store and `/chat` endpoint are unchanged.
- Model: `vertex_ai/gemini-3.5-flash-lite` in the `global` location.
- `/chat` also returns the tool calls the harness made, and the page shows them above the answer.

## Tools (`tools.py`)

| Tool | Source |
| --- | --- |
| `geocode_place` | Open-Meteo geocoding. Returns several candidates (region, country) so "Paris" can be disambiguated. |
| `get_historical_weather` | Open-Meteo archive API. Future trip dates are moved back whole years to the latest year the archive has; each day gets an `outdoor_ok` flag (dry, 50-90F). |
| `read_my_itineraries` | Returns `context.md`, a short style summary built from `Example Itineraries/` by `uv run build_context.py` (rerun after changing a trip). With a keyword, or if `context.md` is missing or stale, it returns the raw itineraries (links stripped) instead. |
| `get_travel_time` | Nominatim (geocode) + OSRM (driving) + routing.openstreetmap.de (walking). Returns both modes and a `suggested_mode`. A place Nominatim cannot find comes back as an error, which is how the agent drops or replaces made-up places. |

The public OSRM demo server answers every profile with driving times, which is why walking
uses the OpenStreetMap foot server. Weather is grid-based past-year data: typical
conditions, not a forecast.

## Setup

1. A GCP project with billing and the Agent Platform API enabled
   (older docs and the endpoint itself still call it Vertex AI)
2. `gcloud auth application-default login`. The app uses your gcloud default
   project, so run `gemini-hello-world` first to check it.
3. `uv run app.py`, then open http://localhost:8000

Try: "3 days in Seattle starting November 10" (rain turns most days indoor), or
"4 days in Lisbon starting June 10".

None of the APIs need a key. A full plan takes a minute or two, mostly because Nominatim
is limited to one request per second.
