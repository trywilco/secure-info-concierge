import asyncio
import os
from app.database.db_manager import init_db, populate_sample_data

async def setup():
    print("Initializing database...")
    await init_db()
    print("Populating sample data...")
    await populate_sample_data()
    print("Setup complete!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    
    import uvicorn
    print("Starting SecureInfo Concierge server...")
    # Get port from environment variable with fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
