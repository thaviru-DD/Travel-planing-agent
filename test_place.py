from tools.placessvisit import place_to_visit

result = place_to_visit.invoke({
    "location": "Galle",
    "travel_plans": "Traveling from colombo to Galle"
})

print(result)