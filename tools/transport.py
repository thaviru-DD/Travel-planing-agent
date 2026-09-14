from langchain_core.tools import tool
from transport_rag import retrieve_transport_info
from tools.distance import distance


# @tool(
#     "transport",
#     description="Recommend suitable transport options based on route, passenger count, and budget."
# )
# def transport(
#     origin: str,
#     destination: str,
#     budget: float,
#     passengers: int = 1
# ) -> str:
#     """
#     Retrieve suitable transport information and route distance
#     based on the user's travel request.
#     """

#     # 1. Create a query for the RAG system
#     query = f"transport options suitable for {passengers} passengers"

#     # 2. Retrieve relevant transport information
#     results = retrieve_transport_info(query)

#     # 3. Combine retrieved documents into one string
#     transport_info = "\n\n".join(
#         document.page_content
#         for document in results
#     )

#     # 4. Get distance from Google Maps
#     distance_result = distance.invoke({
#         "origin": origin,
#         "destination": destination
#     })

#     # 5. Return all information to the agent
#     return f"""
# Travel information:

# Origin: {origin}
# Destination: {destination}
# Passengers: {passengers}
# Budget: Rs. {budget}

# Distance information:
# {distance_result}

# Available transport information:
# {transport_info}
# """

@tool("transport", description="Recommend suitable transport options based on route, passenger count, and budget.")
def transport(origin: str, destination: str, budget: float, passemgers: int) -> str:
    """
    Retrieve suitable transport information and route distance
    based on the user's travel request.
    """

    return f""" """



