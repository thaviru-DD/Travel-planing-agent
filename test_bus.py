from tools.bus import bus

print(bus.invoke({"origin": "Colombo", "destination": "Kandy", "budget": 3000, "passengers": 5}))
print("-" * 50)
print(bus.invoke({"origin": "Colombo, Sri Lanka", "destination": "Galle, Sri Lanka", "budget": 5000, "passengers": 2}))
print("-" * 50)
print(bus.invoke({"origin": "Colombo", "destination": "Jaffna", "budget": 5000}))