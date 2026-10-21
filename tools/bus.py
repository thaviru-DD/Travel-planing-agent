from langchain_core.tools import tool

from bus_rag import retrieve_bus_info
from tools.distance import distance


@tool(
    "bus",
    description=(
        "Get PUBLIC bus options for a route: bus type, operator, travel time, "
        "departure times, fare per person, total fare and whether it fits the budget. "
        "Not for private/hired buses."
    ),
)
def bus(origin: str, destination: str, budget: float, passengers: int = 1) -> str:
    """origin/destination: city names. budget: LKR. passengers: number of travellers."""

    routes = retrieve_bus_info(origin, destination)
    if not routes:
        return (
            f"No public bus information found for {origin} to {destination}. "
            "Tell the user it is not available. Do not invent routes, fares or times."
        )

    # Distance is optional extra info; don't let an API error break the bus answer
    try:
        distance_result = distance.invoke({"origin": origin, "destination": destination})
    except Exception:
        distance_result = "Distance information not available."

    lines = [f"Public bus options from {origin} to {destination} "
             f"({passengers} passenger(s), budget Rs. {budget:,.0f}):"]
    for r in routes:
        line = (f"- {r['bus_type']} ({r.get('operator', 'unknown operator')}) | "
                f"{r.get('travel_time', 'n/a')} | departures: {r.get('departure_times', 'n/a')}")
        if r["fare"] is not None:
            total = r["fare"] * passengers          # Python does the maths, not the LLM
            fits = "within budget" if total <= budget else "OVER budget"
            line += f" | Rs. {r['fare']:,.0f} per person | Rs. {total:,.0f} total ({fits})"
        else:
            line += " | fare not available"
        if r.get("source", "").startswith("SAMPLE"):
            line += " | (sample data)"
        lines.append(line)

    lines.append(f"\nDistance: {distance_result}")
    return "\n".join(lines)