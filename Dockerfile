# Use Python base image
FROM python:3.10-slim

# Install dependencies for Ollama and Supervisor
RUN apt-get update && apt-get install -y \
    curl wget supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
RUN ollama pull llama3.2:1b

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose backend (8000) + frontend (8501)
EXPOSE 8000
EXPOSE 8501

# Copy Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start Supervisor (runs both backend + frontend)
CMD ["/usr/bin/supervisord"]
