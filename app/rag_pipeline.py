from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_PATH = "data"
VECTOR_PATH = "vectorstore"


def create_vector_store():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found in DATA_PATH!")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(docs, embeddings)

    os.makedirs(VECTOR_PATH, exist_ok=True)
    db.save_local(VECTOR_PATH, index_name=INDEX_NAME)
    print("Vector store created at", VECTOR_PATH)
    return db


import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle

# VECTOR_PATH = "vectorstore"
INDEX_NAME = "index"


# def create_vector_store():
#     # Load documents
#     loader = DirectoryLoader("data", glob="*.md")
#     documents = loader.load()
#
#     # Split into chunks
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     docs = splitter.split_documents(documents)
#
#     # Generate embeddings
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#
#     # Build FAISS vector store
#     db = FAISS.from_documents(docs, embeddings)
#
#     # Save locally
#     os.makedirs(VECTOR_PATH, exist_ok=True)
#     db.save_local(VECTOR_PATH, index_name=INDEX_NAME)
#     print("Vector store created at", VECTOR_PATH)
#     return db


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_file = Path(VECTOR_PATH) / f"{INDEX_NAME}.faiss"

    if not vector_file.exists():
        print("Vectorstore not found, creating a new one...")
        db = create_vector_store()  # make sure this returns FAISS object
        if db is None:
            raise RuntimeError("Vectorstore creation failed!")
        return db

    # Load existing vector store
    db = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
        index_name=INDEX_NAME
    )
    if db is None:
        raise RuntimeError("Failed to load existing vectorstore!")
    return db