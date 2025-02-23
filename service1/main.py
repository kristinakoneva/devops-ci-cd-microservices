from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Service 1!"}

@app.get("/call-service2")
def call_service2():
    try:
        response = requests.get("http://localhost:8002/")
        return {"service1": "Calling Service 2", "response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
