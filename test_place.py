from tools.placessvisit import place_to_visit

result = place_to_visit.invoke({
    "location": "Kandy",
    "travel_plans": "Traveling from colombo to kandy"
})

print(result)