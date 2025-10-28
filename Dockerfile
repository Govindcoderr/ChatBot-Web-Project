# Use a lightweight Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl wget supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# ✅ Copy only backend requirements file first
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies from backend requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# ✅ Copy the entire project
COPY . .

# Expose backend and frontend ports
EXPOSE 8000
EXPOSE 8501

# Copy Supervisor config file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ✅ Start Ollama server + pull model + run backend + frontend
CMD bash -c "ollama serve & sleep 5 && ollama pull llama3.2:1b && /usr/bin/supervisord"
