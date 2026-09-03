import sqlite3

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.tools import tool

#import tools
from tools.placessvisit import place_to_visit
from tools.distance import distance


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
    tools=[place_to_visit, distance, remember, recall],
    checkpointer=checkpointer,
    system_prompt="You are a helpful travel assistant. Use the avilable tools when needed to answer the user's question",
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


