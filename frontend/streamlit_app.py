import streamlit as st
import requests
import time

# 🌐 Backend URLs
BACKEND_URL_CRAWL = "http://127.0.0.1:8000/crawl"
BACKEND_URL_CHAT = "http://127.0.0.1:8000/chat"
BACKEND_URL_CLEAR = "http://127.0.0.1:8000/clear_store"

# 🎨 Page config
st.set_page_config(page_title="💬 Webpage RAG Chatbot", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f7f8fa;
    }
    .main {
        background-color: #f7f8fa;
    }
    .user-bubble {
        background-color: #DCF8C6;
        color: black;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        # background-color: #E8E8E8;
        color: black;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 80%;
        float: left;
        clear: both;
    }
    .section {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🧠 Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# 🌐 Step 1: Crawl Section
with st.expander("🌐 Step 1: Scrape Website (Optional)", expanded=not st.session_state.data_loaded):
    url_input = st.text_input("Enter Website URL", placeholder="https://example.com")
    max_pages = st.number_input("Maximum pages to crawl:", min_value=1, max_value=50, value=5)

    if st.button("🚀 Start Scraping"):
        if url_input.strip():
            with st.spinner("Scraping and storing content..."):
                res = requests.post(BACKEND_URL_CRAWL, json={"url": url_input, "max_pages": max_pages})
            result = res.json()
            if result.get("status") == "success":
                st.success(result["message"])
                st.session_state.data_loaded = True
            else:
                st.error(result.get("message", "An error occurred."))
        else:
            st.warning("Please enter a valid URL.")
    
    # 🧹 Step 3: Clear Database
    st.markdown("---")
    if st.button("🧹 Clear Stored ChromaDB Data"):
     with st.spinner("Clearing data..."):
        res = requests.post(BACKEND_URL_CLEAR)
        result = res.json()
        if result.get("status") == "success":
            st.success(result["message"])
            st.session_state.messages = []
            st.session_state.data_loaded = False
        else:
            st.error(result.get("message", "Failed to clear data."))


# 💬 Chat Section (ChatGPT-style)
st.markdown("## 💬 Ask Questions About the Webpage")

chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# 🗨️ Chat input box
query = st.chat_input("Ask me anything about the scraped website...")

def typing_effect(text, speed=0.01):
    """Simulate typing animation for chatbot responses"""
    placeholder = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(f"<div class='bot-bubble'>{typed_text}</div>", unsafe_allow_html=True)
        time.sleep(speed)
    placeholder.markdown(f"<div class='bot-bubble'>{typed_text}</div>", unsafe_allow_html=True)

if query:
    # Display user message instantly
    st.session_state.messages.append({"role": "user", "content": query})
    st.markdown(f"<div class='user-bubble'>{query}</div>", unsafe_allow_html=True)

    # Fetch answer
    with st.spinner("Generating answer..."):
        try:
            res = requests.post(BACKEND_URL_CHAT, json={"question": query})
            answer = res.json()
            if answer.get("status") == "success":
                bot_reply = answer["answer"]
            else:
                bot_reply = "⚠️ Something went wrong while processing your query. and may be the database is empty."
        except Exception as e:
            bot_reply = f"❌ Error connecting to backend: {e}"

    # Animated typing effect
    typing_effect(bot_reply)

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

