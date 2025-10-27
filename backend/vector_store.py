import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from multiprocessing import Pool, cpu_count

def _embed_chunk(chunk):
    """
    Helper function that runs in a separate process to embed a text chunk.
    It creates its own embedding model inside the process.
    """
   
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return model.embed_query(chunk)

def store_text(text_list):
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection("web_knowledge")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    # Use available CPU cores efficiently
    num_workers = max(2, cpu_count() - 1)  # leave one core free
    
    for idx, text in enumerate(text_list):
        chunks = splitter.split_text(text)

        #  Use multiprocessing pool to parallelize embedding computation
        with Pool(processes=num_workers) as pool:
            embeddings = pool.map(_embed_chunk, chunks)

        # Add to ChromaDB
        collection.add(
            documents=chunks,
            ids=[f"{idx}-{i}" for i in range(len(chunks))],
            embeddings=embeddings
        )

def clear_vector_store():
    """
    Deletes all stored content in the ChromaDB collection.
    """
    client = chromadb.PersistentClient(path="chroma_db")
    collection_name = "web_knowledge"

    if collection_name in [c.name for c in client.list_collections()]:
        client.delete_collection(collection_name)
        return f"✅ '{collection_name}' collection cleared successfully."
    else:
        return f"⚠️ Collection '{collection_name}' not found."






# ------ old code (for reference) ------

# import chromadb
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# def store_text(text_list):
#     client = chromadb.PersistentClient(path="chroma_db")
#     collection = client.get_or_create_collection("web_knowledge")

#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#     for idx, text in enumerate(text_list):
#         chunks = splitter.split_text(text)
#         collection.add(
#             documents=chunks,
#             ids=[f"{idx}-{i}" for i in range(len(chunks))],
#             embeddings=[embeddings_model.embed_query(chunk) for chunk in chunks]
#         )
        
# def clear_vector_store():
#     """
#     Deletes all stored content in the ChromaDB collection.
#     """
#     client = chromadb.PersistentClient(path="chroma_db")
#     collection_name = "web_knowledge"

#     if collection_name in [c.name for c in client.list_collections()]:
#         client.delete_collection(collection_name)
#         return f"✅ '{collection_name}' collection cleared successfully."
#     else:
#         return f"⚠️ Collection '{collection_name}' not found."



