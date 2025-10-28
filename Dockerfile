# Use a lightweight Python base image
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl wget supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy all files
COPY . .

# Expose backend and frontend ports
EXPOSE 8000
EXPOSE 8501

# Copy Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ✅ Start Ollama first, then pull model *after* container boots
CMD bash -c "ollama serve & sleep 10 && ollama pull llama3.2:1b && /usr/bin/supervisord"
