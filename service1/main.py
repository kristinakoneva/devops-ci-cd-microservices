"""Main module for Service 1.

This FastAPI app serves as Service 1 and communicates with Service 2.
"""

from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    """Returns a welcome message from Service 1."""
    return {"message": "Hello from Service 1!!"}

@app.get("/call-service2")
def call_service2():
    """Calls Service 2 and returns its response."""
    try:
        response = requests.get("http://service2:8002/", timeout=5)
        return {"service1": "Calling Service 2", "response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
