import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Create embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 2. Create or load Chroma database
if not os.path.exists("./train_chroma_db"):

    loader = TextLoader("data/train_data.txt")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = text_splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./train_chroma_db"
    )

else:

    vectorstore = Chroma(
        persist_directory="./train_chroma_db",
        embedding_function=embeddings
    )


# 3. Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)


# 4. Reusable retrieval function
def retrieve_transport_info(query: str):
    return retriever.invoke(query)