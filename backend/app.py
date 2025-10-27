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

# @app.post("/crawl")
# async def crawl(data: CrawlRequest):
#     """
#     Crawl a user-provided URL, scrape content, store in ChromaDB.
#     """
#     url = data.url
#     max_pages = data.max_pages

#     if not url:
#         return {"status": "error", "message": "Please provide a valid URL."}

#     try:
#         # scraped_texts = await crawl_and_scrape(url, max_pages=max_pages)
#         scraped_texts = await asyncio.to_thread(crawl_and_scrape, url, max_pages)

#         if not scraped_texts:
#             return {"status": "error", "message": "No content found on the URL."}

#         store_text(scraped_texts)
#         return {"status": "success", "message": f"Scraped and stored {len(scraped_texts)} pages."}

#     except Exception as e:
#         return {"status": "error", "message": f"⚠️ Error: {str(e)}"}
    
    
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
    """
    query = data.question

    if not query:
        return {"status": "error", "answer": "Please enter a valid question."}

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