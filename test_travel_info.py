from sub_agents.travel_info_agent import travel_info

result = travel_info.invoke({
    "query": "What are some places to visit in Kandy?"
})

print(result)