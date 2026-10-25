from langchain_core.tools import tool

from train_rag import retrieve_train_info
from tools.distance import distance


@tool(
    "train",
    description=(
        "Recommend suitable public train options based on the route, "
        "number of passengers, and travel budget. Also retrieve "
        "route distance information."
    )
)
def train(
    origin: str,
    destination: str,
    budget: float,
    passengers: int = 1
) -> str:
    """
    Retrieve public train information from the train RAG
    and get distance information for the requested route.
    """

    # 1. Create a query for the Train RAG system
    query = (
        f"Suitable train options from {origin} to {destination}. "
        f"Number of passengers: {passengers}. "
        f"Travel budget: Rs. {budget}. "
        "Include available train routes, train types, "
        "fares, schedules, and travel information."
    )

    # 2. Retrieve relevant train information
    results = retrieve_train_info(query)

    # 3. Combine retrieved documents
    if results:
        train_info = "\n\n".join(
            document.page_content
            for document in results
        )
    else:
        train_info = (
            "No relevant train information was found "
            "in the train knowledge base."
        )

    # 4. Retrieve distance information
    distance_result = distance.invoke({
        "origin": origin,
        "destination": destination
    })

    # 5. Return information to the main agent
    return f"""
Train Recommendation Request

Origin: {origin}
Destination: {destination}
Passengers: {passengers}
Budget: Rs. {budget}

Distance Information:
{distance_result}

Retrieved Train Information:
{train_info}

Recommend suitable public train options using only
the retrieved information.

Do not invent:
- train fares
- train schedules
- train availability
- train travel times
- train operators
"""