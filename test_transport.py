
from tools.transport import transport

result = transport.invoke({
    "origin": "Colombo",
    "destination": "Kandy",
    "budget": 10000,
    "passengers": 2
})

print("Transport Tool Test")
print("-" * 35)
print(result)
