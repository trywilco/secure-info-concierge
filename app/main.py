from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
import asyncio
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.api.routes import router as api_router
from app.auth.routes import router as auth_router
from app.auth.jwt import get_current_user
from app.database.db_manager import init_db, populate_sample_data

# Global variable to track application readiness
app_ready = False
startup_time = time.time()

# Initialize database on startup
@asyncio.coroutine
def setup_db():
    print("Initializing database...")
    yield from init_db()
    print("Populating sample data...")
    yield from populate_sample_data()
    print("Database setup complete!")

app = FastAPI(title="SecureInfo Concierge", description="Financial assistant application with LLM integration")

@app.on_event("startup")
async def startup_event():
    global app_ready, startup_time
    startup_time = time.time()
    
    print("\n" + "="*50)
    print("STARTING SECURE INFO CONCIERGE APPLICATION")
    print("="*50)
    print("Initializing services...")
    
    # Setup database
    start_time = asyncio.get_event_loop().time()
    await setup_db()
    db_time = asyncio.get_event_loop().time() - start_time
    print(f"Database initialization completed in {db_time:.2f} seconds")
    
    # Log Azure OpenAI configuration
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "Not set")
    azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "Not set")
    azure_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "Not set")
    print(f"Azure OpenAI Configuration:")
    print(f"  - Endpoint: {azure_endpoint}")
    print(f"  - Deployment: {azure_deployment}")
    print(f"  - API Version: {azure_api_version}")
    
    print("All services initialized successfully!")
    print("="*50 + "\n")
    
    # Set the app as ready after all initialization is complete
    # Note: This will be set to True after all models are loaded
    # The models are loaded when the first request comes in
    # app_ready will be set to True in the /ready endpoint

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.get("/health")
async def health_check():
    """Simple health check endpoint that always returns 200 OK"""
    return {"status": "ok"}

@app.get("/ready")
async def ready_check():
    """Readiness check endpoint that returns 200 only when the app is fully initialized"""
    global app_ready
    
    # If app is already marked as ready, return 200
    if app_ready:
        return {"status": "ready", "uptime": f"{time.time() - startup_time:.2f} seconds"}
    
    # Check if models are loaded by importing the LLM service
    # This will trigger the model loading if it hasn't happened yet
    try:
        from app.models.llm_service import LLMService
        # Create an instance to ensure models are loaded
        _ = LLMService()
        # If we get here, models are loaded successfully
        app_ready = True
        return {"status": "ready", "uptime": f"{time.time() - startup_time:.2f} seconds"}
    except Exception as e:
        # If models are still loading, return 503 Service Unavailable
        return JSONResponse(
            status_code=503,
            content={
                "status": "initializing",
                "message": "Application is still initializing. Please try again later.",
                "uptime": f"{time.time() - startup_time:.2f} seconds"
            }
        )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # We'll handle authentication in the frontend
    return templates.TemplateResponse("dashboard.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
