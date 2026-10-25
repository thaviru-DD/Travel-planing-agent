from train_rag import retrieve_train_info

query = "Train options from Colombo to Kandy"

results = retrieve_train_info(query)

print("Retrieved Train Information:")
print("-" * 40)

if results:
    for document in results:
        print(document.page_content)
        print("-" * 40)
else:
    print("No train information found.")