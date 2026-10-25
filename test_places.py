
from tools.places_to_visit import place_to_visit

result = place_to_visit.invoke({
    "location": "Kandy, Sri Lanka",
    "travel_plans": "What are the places we can visit in Knady"
})

print("Places to Visit Tool Test")
print("-" * 35)
print(result)
