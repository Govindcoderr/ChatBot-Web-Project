# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some ML + sentence-transformers)
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Install Ollama (if deploying on your own server or Render with Docker)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pull your model (llama3.2:1b)
RUN ollama pull llama3.2:1b

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Copy supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start Ollama + both services
CMD ollama serve & supervisord -c /etc/supervisor/conf.d/supervisord.conf
