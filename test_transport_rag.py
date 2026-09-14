from transport_rag import retrieve_transport_info


query = "Which transport is suitable for 2 passengers?"

results = retrieve_transport_info(query)


for i, document in enumerate(results):
    print(f"\n--- Result {i + 1} ---")
    print(document.page_content)