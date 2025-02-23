"""Main module for Service 2.

This FastAPI app serves as Service 2 and responds to incoming requests.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """Returns a welcome message from Service 2."""
    return {"message": "Hello from Service 2!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
