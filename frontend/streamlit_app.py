import streamlit as st
import requests

st.set_page_config(page_title="🌐 Webpage RAG Chatbot")
st.title("🌐 Webpage RAG Chatbot")

# Step 1: User provides a URL to scrape
st.header("1️⃣ Enter Website URL to Scrape")
url_input = st.text_input("Website URL (e.g., https://example.com)")
max_pages = st.number_input("Maximum pages to crawl:", min_value=1, max_value=50, value=5)

if st.button("Scrape & Store Content"):
    if url_input:
        with st.spinner("Scraping and storing content..."):
            res = requests.post("http://127.0.0.1:8000/crawl", json={"url": url_input, "max_pages": max_pages})
        result = res.json()
        if result["status"] == "success":
            st.success(result["message"])
        else:
            st.error(result["message"])
    else:
        st.error("Please enter a valid URL.")

# Step 2: Ask questions
st.header("2️⃣ Ask Questions About the Webpage")
query = st.text_input("Enter your question:")

if st.button("Ask Question"):
    if query:
        with st.spinner("Generating answer..."):
            res = requests.post("http://127.0.0.1:8000/chat", json={"question": query})
        answer = res.json()
        if answer["status"] == "success":
            st.markdown(f"**Answer:** {answer['answer']}")
        else:
            st.error(answer.get("answer", "An error occurred."))
    else:
        st.error("Please enter a question.")

st.header("3️⃣ Clear Stored Content (Optional)")
if st.button("Clear Old ChromaDB Data"):
    with st.spinner("Clearing stored data..."):
        res = requests.post("http://127.0.0.1:8000/clear_store")
        result = res.json()
        if result["status"] == "success":
            st.success(result["message"])
        else:
            st.error(result["message"])
