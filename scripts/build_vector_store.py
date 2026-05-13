import os
import glob
import hashlib
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from functools import lru_cache


data_dir = Path(__file__).parent.parent / "data"


@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def fetch_documents() -> list:
    """Load all .md files from every sub-folder of KNOWLEDGE_BASE.
    Each document gets a `doc_type` metadata key equal to its parent folder name.
    """
    target_dir = data_dir / "knowledge_base"
    folders    = glob.glob(str(target_dir / "*"))
    documents  = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader   = DirectoryLoader(
            folder,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        for doc in loader.load():
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    return documents


def create_chunks(documents):
    """Split documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    return splitter.split_documents(documents)


def _chunk_hash(chunk) -> str:
    """Stable SHA-256 fingerprint for a chunk (source path + content)."""
    raw = f"{chunk.metadata.get('source', '')}::{chunk.page_content}"
    return hashlib.sha256(raw.encode()).hexdigest()


def _collection_stats(vectorstore) -> tuple[int, int]:
    """Return (count, dimensions) for a Chroma vectorstore."""
    collection      = vectorstore._collection
    count           = collection.count()
    sample          = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions      = len(sample)
    return count, dimensions

def create_embeddings_from_kb():
    """
    Drop the existing Chroma collection (if any), re-embed every chunk from
    scratch, and persist the new collection.
    """
    vector_store_path = data_dir / "vector_store"

    print(f"Creating embeddings from knowledge base... at {vector_store_path}") 
    
    # Remove existing collection (if any)
    if os.path.exists(vector_store_path):
        Chroma(
            persist_directory=vector_store_path,
            embedding_function=get_embeddings(),
        ).delete_collection()


 # Load documents and create chunks
    documents = fetch_documents()
    chunks = create_chunks(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        #collection_name="knowledge_base",
        persist_directory=vector_store_path,
    )
    count, dimensions = _collection_stats(vectorstore)
    print(f"Vector store created with {count} chunks and {dimensions} dimensions.")

   
if __name__ == "__main__":
    create_embeddings_from_kb()