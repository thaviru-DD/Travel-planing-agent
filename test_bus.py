from tools.bus import bus

result = bus.invoke({
    "origin": "Colombo",
    "destination": "Galle",
    "budget": 5000,
    "passengers": 2
})

print("Bus Tool Test")
print("-" * 30)
print(result)
