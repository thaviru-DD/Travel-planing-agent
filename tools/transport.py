from langchain_core.tools import tool
from transport_rag import retrieve_transport_info
from tools.distance import distance


@tool(
    "transport",
    description="Recommend suitable transport options based on route, passenger count, and budget."
)
def transport(
    origin: str,
    destination: str,
    budget: float,
    passengers: int = 1
) -> str:

    # Get transport information from RAG
    query = f"transport options for {passengers} passengers"

    results = retrieve_transport_info(query)

    print("\nRetrieved transport information:")

    for document in results:
        print(document.page_content)

    # Get distance from Google Maps
    distance_result = distance.invoke({
        "origin": origin,
        "destination": destination
    })

    print("\nDistance result:")
    print(distance_result)

    return "Transport tool is working."