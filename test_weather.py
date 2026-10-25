
from tools.weather import weather

result = weather.invoke({
    "location": "Kandy, Sri Lanka",
    "date": "2026-10-25"
})

print("Weather Tool Test")
print("-" * 30)
print(result)
