from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.crawler_scraper import crawl_and_scrape
from backend.rag_pipeline import generate_answer, store_text
from pydantic import BaseModel
class CrawlRequest(BaseModel):
    url: str
    max_pages: int = 10  # default to 10 if not provided

class ChatRequest(BaseModel): 
    question: str

from backend.vector_store import clear_vector_store
import asyncio

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.post("/crawl")
async def crawl(data: CrawlRequest):
    """
    Crawl a user-provided URL, scrape content, store in ChromaDB.
    """
    url = data.url
    max_pages = data.max_pages

    if not url:
        return {"status": "error", "message": "Please provide a valid URL."}

    try:
        # Await the async crawler properly
        scraped_texts = await crawl_and_scrape(url, max_pages=max_pages)

        if not scraped_texts:
            return {"status": "error", "message": "No content found on the URL."}

        # Store results in ChromaDB
        store_text(scraped_texts)

        return {"status": "success", "message": f"Scraped and stored {len(scraped_texts)} pages."}

    except Exception as e:
        return {"status": "error", "message": f"⚠️ Error: {str(e)}"}


@app.post("/chat")
async def chat(data: ChatRequest):
    """
    Ask a question; use RAG to generate answer from stored webpage content.
    Handles small talk and fallback to RAG-based answers.
    """
    query = data.question.strip().lower()

    if not query:
        return {"status": "error", "answer": "Please enter a valid question."}

    # 💬 Small Talk Responses
    small_talk = {
        "hii": "Hey there 👋! How can I help you today?",
        "hello": "Hello! 😊 What would you like to ask?", 
        "hey": "Hey! 👋 What’s up?",
        "how are you": "I'm doing great, thanks for asking 😄! How about you?",
        "who are you": "I'm your Web RAG Assistant 🤖 — here to answer questions about websites you provide.",
        "thank you": "You're very welcome! 🙏",
        "thanks": "Anytime 😊",
        "good morning": "Good morning ☀️! Hope you have a productive day.",
        "good evening": "Good evening 🌙! How’s your day going?",
        "good night": "Good night 🌟! Sleep well.",
        "what is your name": "I'm your Web RAG Assistant 🤖.",
        "help": "Sure! Ask me anything about the webpage you provided or let me know how I can assist you.",
        "who are you": "I'm your Web RAG Assistant 🤖 — here to answer questions about websites you provide.",
        "what can you do": "I can help you find information from the webpages you've provided by answering your questions based on their content.",
        "are you real?": "I'm as real as your friendly neighborhood chatbot 🤖!",
        "do you like me": "I like helping you! 😊",
        "what’s the time": "I don't have a watch, but I'm always here to help you! ⏰",
        "how to use you": "Step 1️⃣: Enter a website URL → Step 2️⃣: Ask me anything about it!",
        "what can you do": "I can help you find information from the webpages you've provided by answering your questions based on their content.",
    }

    for key, value in small_talk.items():
        if key in query:
            return {"status": "success", "answer": value}

    # 🧠 If not small talk, use RAG-based answer
    try:
        answer = generate_answer(query)
        return {"status": "success", "answer": answer}
    except Exception as e:
        return {"status": "error", "answer": f"⚠️ Error: {str(e)}"}

@app.post("/clear_store")
async def clear_store():
    """
    Clears all old stored content in ChromaDB.
    """
    try:
        msg = clear_vector_store()
        return {"status": "success", "message": msg}
    except Exception as e:
        return {"status": "error", "message": f"⚠️ Error: {str(e)}"}
    

@app.get("/health")
def health_check():
    return {"status": "ok"}
