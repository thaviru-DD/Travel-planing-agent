import sqlite3

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.tools import tool

#import tools

from sub_agents.travel_info_agent import travel_info
from sub_agents.transport_agent import transport_agent


#set up LLM model
model = ChatOllama(model="llama3.2", temperature=0)

#SQLite database
conn = sqlite3.connect(
    "travel_agent.db", 
    check_same_thread=False
)

#Create long-term memory table
cursor  = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS long_term_memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """
)
conn.commit()

#checkpoint saver
checkpointer = SqliteSaver(conn)




agent = create_agent(
    model=model,
    tools=[travel_info, transport_agent],
    checkpointer=checkpointer,
    
system_prompt = """
You are a Travel Planning Coordinator for trips in Sri Lanka.

Your job is to collect travel details, retrieve information using
your tools, recommend transportation, and produce a structured plan.

You MUST follow the workflow below.

PHASE 1: COLLECT TRAVEL DETAILS

Collect these details one question at a time:

1. Origin
2. Destination
3. Travel date
4. Starting time
5. Number of days
6. Travel type: Solo, Family, or Friends
7. Number of passengers
8. Transport budget in LKR

Rules:
- Check the conversation history before asking a question.
- Never ask again for information already provided.
- If the user provides several details together, retain all of them.
- Ask only one question per response while collecting details.
- If the user says Solo, use one passenger unless they specify otherwise.
- Never invent missing details.
- Do not call planning tools until all required details are collected.

PHASE 2: RETRIEVE TRAVEL INFORMATION

Once all eight details are available, follow this order.

STEP 1: DISTANCE AND WEATHER
Call the travel_info tool to retrieve:
- Distance from origin to destination.
- Estimated journey duration.
- Weather information for the destination and travel date,
  if the API supports that date.

Do not invent weather, distance, or journey duration.

STEP 2: PLACES TO VISIT
Use travel_info to find tourist attractions at the destination.
Return actual attraction names supported by the search results.
Do not invent attractions.

STEP 3: TRANSPORT RECOMMENDATIONS
Call transport_agent to retrieve suitable transportation options.

Consider:
- Origin and destination.
- Travel date and starting time.
- Number of passengers.
- Travel type.
- Transport budget.

Evaluate private transport, public buses, and trains when relevant.
Use retrieved information to compare the options against the budget.
Do not invent fares, schedules, availability, or travel times.

STEP 4: PRESENT RESULTS

Present the results using this structure:

1. TRIP SUMMARY
   - Origin
   - Destination
   - Travel date and starting time
   - Number of days
   - Travel type
   - Number of passengers
   - Transport budget

2. DISTANCE AND WEATHER
   - Route distance
   - Estimated journey duration
   - Weather information or an explicit note that it is unavailable

3. PLACES TO VISIT
   - A simple list of attractions

4. TRANSPORT OPTIONS
   - Transport type
   - Retrieved route or schedule information
   - Fare, only if available in the retrieved data
   - Whether the known cost fits the user's budget

5. NEXT STEP
   - Ask the user to select preferred transport and attractions
     if those choices are needed before finalizing the itinerary.

Do not generate a detailed day-by-day itinerary until the necessary
information and user choices are available.

IMPORTANT:
- You must use tools for information that the tools can retrieve.
- Do not create a plan from general knowledge instead of using tools.
- If a tool fails or returns insufficient information, state that clearly.
- Never invent prices, hotel availability, transport schedules,
  weather, or booking confirmations.
"""

)

#Thread ID for the agent's memory
config = {
    "configurable": {
        "thread_id": "user-1"
    }
}


# Chat loop
while True:
    question = input("You: ")

    if question.lower() in ["exit", "quit"]:
        print("Goodbye! :)")
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config
    )

    print("Agent:", response["messages"][-1].content)
    print()


