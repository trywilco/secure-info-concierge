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

# Create a default .env file with configuration settings
RUN echo "# Engine Wilco AI Configuration\nENGINE_BASE_URL=https://engine.wilco.gg\nWILCO_ID=620ba777a0cccde6931ad14d\n\n# The ENGINE_WILCO_AI_URL will be constructed as:\n# \${ENGINE_BASE_URL}/users/\${WILCO_ID}/wilcoAiConfig" > /app/.env

EXPOSE 8000

# Start the application without running the model download first
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app"]
