FROM python:3.9-slim

WORKDIR /app

# Install development dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir watchdog

# Create data directory
RUN mkdir -p /app/data

# Copy the application
COPY . .

# Create a default .env file with Azure OpenAI settings
RUN echo "# Azure OpenAI API Configuration\nAZURE_OPENAI_ENDPOINT=https://wilco-ai.openai.azure.com\nAZURE_OPENAI_API_KEY=fec412fcb1f14812b7416e74ae7c0f6b\nAZURE_OPENAI_DEPLOYMENT=gpt-4o-mini\nAZURE_OPENAI_API_VERSION=2025-01-01-preview" > /app/.env

EXPOSE 8000

# Start the application without running the model download first
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app"]
