# ---- Base image ----
FROM python:3.10.11-slim

# ---- Set work directory ----
WORKDIR /app

# ---- Install system dependencies (optional but useful) ----
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy your backend code ----
COPY backend/ ./backend/
COPY backend/requirements.txt ./requirements.txt

# ---- Install Python dependencies ----
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ---- Expose port ----
EXPOSE 8000

# ---- Start FastAPI server ----
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
