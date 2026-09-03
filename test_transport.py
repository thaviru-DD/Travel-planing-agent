from tools.transport import transport


result = transport.invoke({
    "origin": "Colombo, Sri Lanka",
    "destination": "Kandy, Sri Lanka",
    "budget": 10000,
    "passengers": 2
})

print(result)

