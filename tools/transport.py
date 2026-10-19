
from langchain_core.tools import tool

from transport_rag import retrieve_transport_info
from tools.distance import distance


@tool(
    "transport",
    description=(
        "Recommend suitable transport options based on the route, "
        "number of passengers, and travel budget. Also retrieve "
        "route distance information."
    )
)
def transport(
    origin: str,
    destination: str,
    budget: float,
    passengers: int = 1
) -> str:
    """
    Retrieve transport options from the transport knowledge base
    and get distance information for the requested route.
    """

    # 1. Create a query for the transport RAG system
    query = (
        f"Suitable transport options for {passengers} passengers. "
        f"Travel budget: Rs. {budget}. "
        "Include available transport types and their cost information."
    )

    # 2. Retrieve relevant transport information
    results = retrieve_transport_info(query)

    # 3. Combine the retrieved documents
    if results:
        transport_info = "\n\n".join(
            document.page_content
            for document in results
        )
    else:
        transport_info = (
            "No relevant transport information was found "
            "in the transport knowledge base."
        )

    # 4. Retrieve distance information
    distance_result = distance.invoke({
        "origin": origin,
        "destination": destination
    })

    # 5. Return the results to the main agent
    return f"""
Transport Recommendation Request

Origin: {origin}
Destination: {destination}
Passengers: {passengers}
Budget: Rs. {budget}

Distance Information:
{distance_result}

Retrieved Transport Information:
{transport_info}

Recommend suitable options using the retrieved information.
Do not invent prices or transport availability.
"""
