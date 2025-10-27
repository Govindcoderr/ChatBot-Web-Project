# ChatBot Web Project

This project implements a chatbot using a Retrieval-Augmented Generation (RAG) approach. It consists of a backend API built with FastAPI and an optional frontend user interface developed with Streamlit.

## Project Structure

```
chatbot-web-project
├── backend
│   ├── app.py                # Entry point for the FastAPI API server
│   ├── rag_pipeline.py       # Logic for the RAG process
│   ├── vector_store.py       # Setup for embedding and vector database
│   ├── crawler_scraper.py    # Website crawling and scraping functionality
│   └── requirements.txt      # Project dependencies for the backend
├── frontend
│   └── streamlit_app.py      # Optional chat UI built with Streamlit
├── README.md                 # Project documentation
└── .gitignore                # Files and directories to ignore by Git
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd chatbot-web-project
   ```

2. **Set up a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install backend dependencies:**
   ```
   pip install -r backend/requirements.txt
   ```

4. **Run the FastAPI server:**
   ```
   uvicorn backend.app:app --reload
   ```

5. **Run the Streamlit app (optional):**
   ```
   streamlit run frontend/streamlit_app.py
   ```

## Usage Guidelines

- Access the FastAPI documentation at `http://localhost:8000/docs` to interact with the API endpoints.
- Use the Streamlit app to chat with the bot through the user interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.