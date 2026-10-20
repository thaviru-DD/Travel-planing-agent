from tools.weather import weather

result = weather.invoke({
    "location": "Colombo, Sri Lanka",
    "date": "2026-10-20"
})

print(result)