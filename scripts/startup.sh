#!/bin/bash

echo "=== Starting Secure Info Concierge application ==="
echo "Initializing application on port 8000..."

# Download models before starting the application
echo ""
echo "=== Pre-downloading ML models ==="
if [ -d "$HOME/.cache/huggingface/hub" ]; then
    echo "✅ HuggingFace model cache found. Using cached models."
else
    echo "⚠️ HuggingFace model cache not found."
    echo "🔄 Downloading models now..."
    # Run the model downloader with smaller batch sizes to avoid memory issues
    python -m app.models.download_models
    if [ $? -ne 0 ]; then
        echo "⚠️ Warning: Model pre-download had issues. Models will be downloaded on first use."
    else
        echo "✅ Models successfully pre-downloaded!"
    fi
fi

echo ""
echo "=== Starting FastAPI application ==="
# Start the application with hot reloading
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app
