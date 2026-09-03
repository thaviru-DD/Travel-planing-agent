from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# --------------------------------------------------
# 1. Load transport data
# --------------------------------------------------

loader = TextLoader("data/transport_data.txt")
documents = loader.load()


# --------------------------------------------------
# 2. Split into chunks
# --------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = text_splitter.split_documents(documents)


# --------------------------------------------------
# 3. Create embedding model
# --------------------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# --------------------------------------------------
# 4. Create / connect to Chroma vector database
# --------------------------------------------------

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)


# --------------------------------------------------
# 5. Create retriever
# --------------------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)


# --------------------------------------------------
# 6. Function used by transport.py
# --------------------------------------------------

def retrieve_transport_info(query: str):
    """
    Retrieve relevant transport information
    from the transport knowledge base.
    """

    return retriever.invoke(query)