import chromadb
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def store_text(text_list):
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection("web_knowledge")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    for idx, text in enumerate(text_list):
        chunks = splitter.split_text(text)
        #batch embed all  chunks (faster then looping )
        embeddings =embeddings_model.embed_documents(chunks)
        collection.add(
            documents=chunks,
            ids=[f"{idx}-{i}" for i in range(len(chunks))],
            # embeddings=[embeddings_model.embed_query(chunk) for chunk in chunks]
            embeddings=embeddings
        )

def retrieve_context(query):
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_collection("web_knowledge")
    results = collection.query(query_texts=[query], n_results=5)
    return "\n".join(results["documents"][0])

def generate_answer(query):
    context = retrieve_context(query)
    llm = ChatOllama(model="llama3.2:1b" ,temperature=0)
    prompt = f"Use this website information to answer:\n\n{context}\n\nQuestion: {query}"
    return llm.invoke(prompt).content
