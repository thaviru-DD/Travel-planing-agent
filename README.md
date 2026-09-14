# Travel Planning Agent

A Python travel assistant that uses LangChain, LangGraph, Ollama, and Tavily to answer travel questions and find places to visit.

## Requirements

- Python 3.9 or newer
- Ollama
- The Ollama chat model `llama3.2`
- The Ollama embedding model `nomic-embed-text` for transport retrieval
- A Tavily API key

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Install and start Ollama, then download the model used by the agent:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Create a `.env` file in the project root:

```dotenv
TAVILY_API_KEY=your_tavily_api_key
```

Keep `.env` private. It is excluded from Git by `.gitignore`.

## Run the agent

Start the assistant from the project root:

```bash
./.venv/bin/python agent.py
```

Enter a travel question when prompted, for example:

```text
Suggest places to visit in Kandy for a two-day trip.
```

The agent currently uses the places and distance tools and stores conversation
memory in `travel_agent.db`.

## Transport retrieval

Transport retrieval uses the existing Chroma database in `chroma_db/` and the
`nomic-embed-text` Ollama embedding model. The transport tool can be used from
Python, but it is not currently registered in `agent.py`.

## Check dependencies

```bash
./.venv/bin/python -m pip check
```

## Project structure

```text
.
├── README.md
├── agent.py
├── requirements.txt
├── transport_rag.py
├── chroma_db/
├── data/
│   └── transport_data.txt
├── sub_agents/
│   ├── accommodation_agent.py
│   ├── public_transport_agent.py
│   └── travel_info_agent.py
├── test_transport.py
├── test_transport_rag.py
├── tools/bus_schedule.py
├── tools/calculator.py
├── tools/distance.py
├── tools/hotel_avilability.py
├── tools/hotel_search.py
├── tools/places_to_visit.py
├── tools/ticket_price.py
├── tools/train_schedule.py
├── tools/transport.py
└── tools/weather.py
```

# Travel Planning Agent Workflow

## Example User Request

```text
I need to visit Kandy. Can you create a travel plan for me?
```

The Travel Planning Agent should gather the required information first and then create the travel plan step by step.

---

## 1. Ask Follow-Up Questions

Before generating the travel plan, the agent should ask the user:

1. What date and time would you like to start your journey?
2. How many days would you like to stay and travel in Kandy?
3. Are you travelling:

   * Solo
   * With family
   * With friends
4. If travelling with family or friends, how many people will be travelling?

The answers to these questions should be used when recommending transportation, places to visit, accommodation, and other travel arrangements.

---

# 2. Calculate Distance and Travel Duration

The agent should identify the user's origin and destination.

Example:

```text
Origin: Colombo
Destination: Kandy
```

The agent should then use the distance tool to provide:

* Distance from the origin to Kandy
* Estimated travel duration

Example:

```text
Distance: 115 km
Estimated travel time: 3 hours
```

---

# 3. Recommend Transportation

The agent should recommend suitable transportation methods based on:

* Number of travellers
* Budget
* Distance
* Weather conditions
* User preference

Possible transportation methods include:

* Car
* Van
* Bike
* Bus
* Train

---

## Family or Friends Trip

If the user is travelling with family or friends, the agent should ask:

```text
How many people are travelling with you?
```

The agent should then recommend suitable transportation based on the number of passengers and the user's budget.

For example:

```text
2 people → Bike or Car

4 people → Car

6 people → Van

Large group → Bus
```

The agent may also present alternative transportation methods and allow the user to choose.

---

## Solo Trip

If the user is travelling alone, the agent should recommend options such as:

* Bike
* Car
* Bus
* Train

The user should then be allowed to select the preferred transportation method.

---

# 4. Bike Travel Flow

If the user selects a **bike**, the agent should check the weather conditions for the route and travel date.

The Weather Tool should check information such as:

* Rain probability
* General weather condition
* Temperature
* Severe weather conditions, if available

Example:

```text
There is a high probability of rain during your journey.

Travelling by bike may not be the safest or most comfortable option.
I recommend considering a car, bus, or train instead.
```

If the weather conditions are suitable, the agent can confirm that travelling by bike is a reasonable option.

---

# 5. Bus Travel Flow

If the user selects **bus**, the agent should first ask:

```text
Would you like to use public transport or hire a private bus?
```

## Public Bus

If the user selects public transport, the agent should provide available information such as:

* Bus departure times
* Starting location / bus station
* Destination
* Estimated travel duration
* Ticket price per passenger
* Total ticket price based on the number of travellers

Example:

```text
Departure: 8:00 AM
Starting point: Colombo
Destination: Kandy
Ticket price: Rs. XXXX per person
```

If a supported booking service is connected, the agent may then ask:

```text
Would you like me to book the bus for you?
```

A booking should only be performed after the user explicitly confirms the booking details.

---

## Private / Hired Bus

If the user selects a hired bus, the agent should provide suitable private transport options based on:

* Number of passengers
* Distance
* Estimated cost
* Budget

---

# 6. Train Travel Flow

If the user selects **train**, the agent should retrieve available train information for the selected travel date.

The agent should provide:

* Departure times
* Departure station
* Destination station
* Estimated journey duration
* Ticket price
* Ticket price for all travellers, when applicable

Example:

```text
Departure station: Colombo Fort
Destination: Kandy
Departure time: 7:00 AM
Ticket price: Rs. XXXX per person
```

If train booking is supported through a connected booking service, the agent may ask:

```text
Would you like me to book the train for you?
```

The booking should only proceed after explicit user confirmation.

---

# 7. Recommend Places to Visit

After transportation is determined, the agent should recommend places to visit in Kandy.

For example:

```text
Suggested places:

1. Temple of the Tooth
2. Kandy Lake
3. Royal Botanical Gardens
4. Bahirawakanda Temple
```

The agent should allow the user to select which places they would like to include in the trip.

The selected locations can then be used when creating the final itinerary.

---

# 8. Accommodation Decision

The agent should use the number of travel days to determine whether accommodation is required.

## One-Day Trip

If the user is travelling only for one day:

```text
Hotel recommendation is not required.
```

The agent can create a one-day itinerary using the selected attractions and transportation method.

---

## Multi-Day Trip

If the trip is longer than one day, the agent should search for accommodation in Kandy.

Hotel recommendations should consider:

* Number of travellers
* Travel dates
* User budget
* Hotel price
* Location
* Availability

Example:

```text
Hotel A
Price: Rs. XXXX per night

Hotel B
Price: Rs. XXXX per night

Hotel C
Price: Rs. XXXX per night
```

If the user selects a hotel and a supported hotel-booking integration is available, the agent may ask:

```text
Would you like me to book this hotel for you?
```

The booking should only happen after the user explicitly confirms the hotel, dates, number of guests, price, and other relevant booking details.

---

# 9. Generate the Final Travel Plan

Once the required information has been collected, the agent should create a complete itinerary.

Example:

```text
Kandy Travel Plan

Starting Location:
Colombo

Destination:
Kandy

Travel Date:
September XX, 2026

Travellers:
2 people

Transportation:
Car

Distance:
115 km

Estimated Travel Time:
3 hours

Day 1:
- Leave Colombo at 7:00 AM
- Arrive in Kandy at approximately 10:00 AM
- Visit Temple of the Tooth
- Visit Kandy Lake
- Lunch
- Visit Royal Botanical Gardens

Hotel:
Selected hotel

Day 2:
- Breakfast
- Visit selected attractions
- Begin return journey
```

---

# Agent Workflow

```text
User Request
     │
     ▼
Ask Follow-Up Questions
     │
     ├── Travel date/time
     ├── Number of days
     ├── Solo / Family / Friends
     └── Number of travellers
     │
     ▼
Calculate Distance + Duration
     │
     ▼
Recommend Transportation
     │
     ├── Bike
     │     └── Check Weather
     │
     ├── Bus
     │     ├── Public
     │     │    └── Schedule + Fare + Optional Booking
     │     └── Private
     │
     ├── Train
     │     └── Schedule + Fare + Optional Booking
     │
     ├── Car
     │
     └── Van
     │
     ▼
Recommend Places to Visit
     │
     ▼
User Selects Attractions
     │
     ▼
Check Trip Duration
     │
     ├── 1 Day
     │     └── No Hotel Required
     │
     └── More Than 1 Day
           └── Recommend Hotels
                  │
                  └── Optional Booking
     │
     ▼
Generate Final Travel Itinerary
```

## Important Agent Behaviour

The agent should:

* Ask for missing information instead of guessing important trip details.
* Use available tools and APIs for live information such as distance, weather, transport schedules, ticket prices, hotel availability, and prices.
* Never invent live schedules, prices, availability, or booking confirmations.
* Recommend alternative transport if weather conditions make the selected option unsuitable.
* Consider the number of travellers when recommending transportation.
* Consider the number of travel days when recommending accommodation.
* Ask for explicit confirmation before performing any booking or other external action.
* Present the final travel plan in a clear, structured format.




