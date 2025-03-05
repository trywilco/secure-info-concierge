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

EXPOSE 8000

# Start the application without running the model download first
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app"]
