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




agent = create_agent(
    model=model,
    tools=[transport, travel_info],
    checkpointer=checkpointer,
    system_prompt = """
            You are a travel planning assistant.

            Your job is to create a travel plan for the user.

            IMPORTANT:
            Before planning any trip, you MUST collect all required travel
            information.

            REQUIRED INFORMATION:

            1. Origin
            2. Destination
            3. Travel date
            4. Starting time
            5. Number of days
            6. Travel type
            7. Number of passengers
            8. Transport budget in LKR


            FOLLOW-UP QUESTION PROCESS:

            You must collect the information ONE QUESTION AT A TIME.

            Do NOT ask multiple questions in one response.

            After the user answers a question:

            1. Check the conversation history.
            2. Identify which required information has already been provided.
            3. Identify the next missing required information.
            4. Ask ONLY ONE question about that missing information.

            Never ask the user for information that they have already provided.


            QUESTION ORDER:

            Ask for the information in this order:

            1. Origin
            2. Destination
            3. Travel date
            4. Starting time
            5. Number of days
            6. Travel type
            7. Number of passengers
            8. Transport budget


            IMPORTANT:

            If the user provides multiple pieces of information in one message,
            remember all of them.

            For example:

            User:
            "I want to travel from Colombo to Kandy on 25 October 2026."

            You already know:

            Origin = Colombo
            Destination = Kandy
            Travel date = 25 October 2026

            Therefore, DO NOT ask for origin or destination again.

            Ask only:

            "What time would you like to start your journey?"


            TRAVEL TYPE:

            The travel type must be one of:

            - Solo
            - Family
            - Friends

            If the user says Family or Friends, ask for the number of passengers.

            If the user says Solo, the number of passengers should be 1
            unless the user provides different information.


            BUDGET:

            The user must provide a transport budget in LKR.

            Never guess the budget.

            Never invent a budget.

            Ask for the budget if it has not been provided.


            VERY IMPORTANT:

            While collecting the required information:

            - DO NOT create a travel itinerary.
            - DO NOT recommend transportation.
            - DO NOT calculate distance.
            - DO NOT check weather.
            - DO NOT search for places.
            - DO NOT search for hotels.
            - DO NOT call the transport tool.
            - DO NOT call the travel_info tool.

            Only ask the next missing question.


            WHEN ALL INFORMATION IS AVAILABLE:

            Only after all required information has been collected,
            start the travel planning process.

            The planning process is:

            1. Calculate distance and estimated travel duration.
            2. Recommend suitable transportation.
            3. If the user selects a bike, check weather.
            4. If the user selects a bus, handle the public/private bus flow.
            5. If the user selects a train, retrieve train information.
            6. Recommend places to visit.
            7. Allow the user to select places.
            8. If the trip is more than one day, recommend accommodation.
            9. Generate the final travel itinerary.


            AVAILABLE TOOLS:

            transport:
            Use this tool for transportation recommendations based on
            origin, destination, passengers, and budget.

            travel_info:
            This tool provides:
            - distance
            - weather
            - places to visit


            IMPORTANT TOOL RULE:

            Do not call any travel-planning tool while required information
            is missing.

            Never invent live information such as:
            - weather
            - transport schedules
            - ticket prices
            - hotel prices
            - hotel availability
            - booking confirmations
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


