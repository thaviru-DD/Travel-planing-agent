from langchain_core.tools import tool

@tool("calculator", description="Calculate full traveling costs based on distance, fuel efficiency, and fuel price.")
def claculator(distance: float, fuel_cost: float):
    pass