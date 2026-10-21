"""
Bus knowledge base: parses data/bus_data.txt into one record per route and
looks routes up by EXACT origin + destination (no embeddings, no stale DB).
"""
import re
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "bus_data.txt"   # works from any cwd

FIELDS = {
    "Starting Location": "origin",
    "Destination": "destination",
    "Bus Type": "bus_type",
    "Operator": "operator",
    "Approximate Travel Time": "travel_time",
    "Departure Times": "departure_times",
    "Fare Per Person (LKR)": "fare",
    "Source": "source",
    "Notes": "notes",
}


def clean_place(text: str) -> str:
    """'Colombo, Sri Lanka' -> 'colombo'"""
    return text.split(",")[0].strip().lower()


def load_bus_routes() -> list[dict]:
    text = DATA_FILE.read_text(encoding="utf-8")
    routes = []
    # Every "BUS ROUTE: ..." line starts a new record; keep only the bodies
    for block in re.split(r"(?m)^BUS ROUTE:.*$", text)[1:]:
        record = {}
        for line in block.strip().splitlines():
            key, _, value = line.partition(":")
            if key.strip() in FIELDS:
                record[FIELDS[key.strip()]] = value.strip()
        if "origin" in record and "destination" in record:
            fare = re.search(r"[\d,.]+", record.get("fare", ""))
            record["fare"] = float(fare.group().replace(",", "")) if fare else None
            routes.append(record)
    return routes


def retrieve_bus_info(origin: str, destination: str) -> list[dict]:
    o, d = clean_place(origin), clean_place(destination)
    return [r for r in load_bus_routes()
            if r["origin"].lower() == o and r["destination"].lower() == d]