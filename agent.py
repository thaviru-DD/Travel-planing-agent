from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from tools.placessvisit import place_to_visit

# Set up the LLM
llm = ChatOllama(model="llama3.2", temperature=0)

# Register your tools
tools = [place_to_visit]

#  Difine the agent's system prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant. Use the avilable tools when needed to answer the user's question"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create the agent and executor
agent = create_tool_calling_agent(llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    user_input = input("Enter your travel Question: ")
    result = agent_executor.invoke({"input": user_input})
    print("\nFinal answer:")
    print(result["output"])