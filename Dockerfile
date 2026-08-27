FROM python:3.11-slim

# Install system dependencies: ffmpeg and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    fonts-dejavu-core \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir uvicorn fastapi gTTS pillow google-adk google-genai google-cloud-storage

# Copy application files
COPY app /app/app
COPY frontend /app/frontend

ENV PORT=8080
EXPOSE 8080

CMD ["python", "frontend/main.py"]
