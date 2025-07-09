"""
Main module for Service 2.

This is a simple FastAPI app that Service 1 will call.
"""

from fastapi import FastAPI
import uvicorn
from datetime import datetime, timezone # Import datetime and timezone

app = FastAPI(
    title="Service 2 API",
    description="A simple service that responds to requests from Service 1.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Returns a welcome message from Service 2 with a dynamic timestamp."""
    # Get current UTC time and format it as an ISO 8601 string
    current_timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds') + 'Z'
    return {"message": "Hello from Service 2!", "timestamp": current_timestamp}

if __name__ == "__main__":
    uvicorn.run("service2:app", host="0.0.0.0", port=8002, reload=True)