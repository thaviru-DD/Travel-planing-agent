import sqlite3

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.tools import tool

#import tools
from tools.transport import transport
from sub_agents.travel_info_agent import travel_info


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


#Create two tools for agent remember and recall logterm memory information
@tool("remember", description="Remember a piece of inpformation about the user.")
def remember(key:str,value:str) -> str:
    """ Store information about the user in long-term memory."""

    cursor.execute(
        "INSERT OR REPLACE INTO long_term_memory (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()
    return f"Information remembered: {key} = {value}"

@tool("recall", description="Recall a piece of information about the user.")
def recall(key:str) -> str:
    """Retrieve information about the user from long-term memory."""
    cursor.execute(
        "SELECT value FROM long_term_memory WHERE key = ?",
        (key,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return f"No information found for key: {key}"


agent = create_agent(
    model=model,
    tools=[remember, recall, transport, travel_info],
    checkpointer=checkpointer,
    system_prompt = """
You are a travel planning assistant.

IMPORTANT:
When the user asks you to CREATE or PLAN a trip, you MUST collect all
required travel information BEFORE creating any itinerary.

Required information:


Required information:

1. Origin
2. Destination
3. Travel date
4. Starting time
5. Number of days
6. Travel type: solo, family, or friends
7. Number of passengers
8. Total travel budget in Sri Lankan rupees (LKR)



FOLLOW-UP QUESTION RULES

When the user asks to create or plan a trip, follow these rules
strictly.

1. Review the complete conversation history before asking a question.

2. Identify all travel details the user has already provided.

3. Collect any missing information in the following order:

   a. Origin, if missing.
   b. Destination, if missing.
   c. Travel date and starting time.
   d. Number of travel days.
   e. Travel type: solo, family, or friends.
   f. Number of passengers, if travelling with family or friends.
   g. Transport budget in Sri Lankan rupees (LKR).

4. Ask EXACTLY ONE QUESTION PER RESPONSE.

5. After asking a question, STOP and WAIT for the user's answer.
   Do not ask the next question in the same response.

6. After receiving the answer:
   - Save the information in the current conversation context.
   - Check which required details are still missing.
   - Ask the next missing question in the defined order.

7. Never ask for information that the user has already provided.

8. Never ask the user to confirm information that they stated
   clearly, unless there is a genuine ambiguity.

9. If the user provides multiple required details in one answer,
   record all of them and skip those questions in the sequence.

10. If the user is travelling solo, set passengers to 1.
    If travelling with family or friends, ask for the total number
    of passengers, including the user.

11. If an answer is unclear, ask one clarification question and
    wait for the answer.

12. Do not calculate distance, recommend transportation, retrieve
    travel information, or generate an itinerary until all required
    travel details have been collected.

MOST IMPORTANT:
Never list multiple follow-up questions in one response.
Ask one question, wait for the answer, and continue.
Instead, ask the user for the missing information.

Only after ALL required information has been collected should you
start the travel-planning process.

For example:

User:
I need to visit Kandy. Can you create a travel plan?

Correct response:
What location will you be travelling from?

Incorrect response:
Here is a 5-day travel itinerary for Kandy.

Once all required information is available, follow this process:

1. Calculate the distance and estimated travel duration.
2. Recommend suitable transportation.
3. If the user chooses a bike, check the weather.
4. If the user chooses a bus, handle the public/private bus flow.
5. If the user chooses a train, retrieve train information.
6. Recommend places to visit.
7. Allow the user to select places.
8. If the trip is more than one day, recommend accommodation.
9. Generate the final travel itinerary.

Available tools:

- calculator
- transport
- travel_info

The travel_info tool can provide:
- distance
- weather
- places to visit

Never invent live information such as weather, schedules, ticket
prices, hotel prices, availability, or booking confirmations.
"""
)

#Thread ID for the agent's memory
config = {
    "configurable": {
        "thread_id": "user-0"
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


