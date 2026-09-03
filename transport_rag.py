from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# Embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Connect to existing Chroma database
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


# Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)


def retrieve_transport_info(query: str):
    """
    Retrieve relevant transport information
    from the transport knowledge base.
    """

    results = retriever.invoke(query)

    return results