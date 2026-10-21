from bus_rag import retrieve_bus_info


query = "What buses are available from Colombo to Kandy?"

results = retrieve_bus_info(query)

print("\nRetrieved Bus Information:\n")

for result in results:
    print(result.page_content)
    print("-" * 50)