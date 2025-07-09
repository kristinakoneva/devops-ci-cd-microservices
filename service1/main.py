"""
Main module for Service 1.

This FastAPI app serves as Service 1, provides a modern web UI,
and communicates with a separate Service 2.
"""

import os
import uvicorn
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

# pylint: disable=C0301 # Ignoring line length for embedded HTML/CSS/JS for readability
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Service 1 Interface</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #6a057f; /* Deep Purple */
            --secondary-color: #883997; /* Lighter Purple */
            --accent-color: #ff6f61; /* Coral/Orange */
            --background-light: #f5f0f6;
            --background-card: #ffffff;
            --text-dark: #333333;
            --text-light: #666666;
            --border-color: #e0e0e0;
            --shadow-light: rgba(0, 0, 0, 0.08);
            --shadow-medium: rgba(0, 0, 0, 0.15);
            --success-color: #28a745;
            --error-color: #dc3545;
            --info-color: #007bff;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--background-light);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            color: var(--text-dark);
            text-align: center;
            line-height: 1.6;
        }
        .container {
            background-color: var(--background-card);
            padding: 45px 60px;
            border-radius: 15px;
            box-shadow: 0 10px 30px var(--shadow-light);
            max-width: 550px;
            width: 90%;
            border: 1px solid var(--border-color);
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            color: var(--primary-color);
            margin-bottom: 25px;
            font-weight: 700;
            font-size: 2.5em;
            letter-spacing: -0.5px;
        }
        p {
            font-size: 1.1em;
            margin-bottom: 30px;
            color: var(--text-light);
        }
        .modern-button {
            background: linear-gradient(45deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 18px 35px;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 6px 15px var(--shadow-light);
            outline: none;
        }
        .modern-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px var(--shadow-medium);
            background: linear-gradient(45deg, var(--secondary-color) 0%, var(--primary-color) 100%);
        }
        .modern-button:active {
            transform: translateY(0);
            box-shadow: 0 4px 10px var(--shadow-light);
        }
        #response {
            margin-top: 35px;
            padding: 20px;
            background-color: var(--background-light);
            border-radius: 10px;
            text-align: left;
            font-family: 'Consolas', 'Monaco', monospace;
            white-space: pre-wrap;
            font-size: 0.9em;
            color: var(--text-dark);
            border: 1px solid var(--border-color);
            max-height: 250px;
            overflow-y: auto;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
            transition: background-color 0.3s ease;
        }
        #response.success { border-color: var(--success-color); }
        #response.error { border-color: var(--error-color); }

        .status-message {
            font-weight: 600;
            margin-bottom: 8px;
            display: block;
        }
        .status-message.success { color: var(--success-color); }
        .status-message.error { color: var(--error-color); }
        .status-message.loading { color: var(--info-color); }

        .api-links {
            margin-top: 30px;
            font-size: 0.95em;
            color: var(--text-light);
        }
        .api-links a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 600;
            margin: 0 10px;
            transition: color 0.2s ease, text-decoration 0.2s ease;
        }
        .api-links a:hover {
            color: var(--accent-color);
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Service 1</h1>
        <p>This interface allows you to interact with Service 1 and trigger a call to Service 2.</p>
        <button id="callService2Btn" class="modern-button">Call Service 2</button>
        <div id="response"></div>
        <div class="api-links">
            <a href="/" target="_blank">Service 1 Root API</a> |
            <a href="/docs" target="_blank">API Documentation</a> |
            <a href="/redoc" target="_blank">ReDoc Docs</a>
        </div>
    </div>

    <script>
        document.getElementById('callService2Btn').addEventListener('click', async () => {
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '<span class="status-message loading">Loading response from Service 2...</span>';
            responseDiv.className = ''; // Reset classes
            
            try {
                const response = await fetch('/call-service2');
                const data = await response.json();

                if (response.ok) {
                    responseDiv.innerHTML = '<span class="status-message success">Success:</span><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    responseDiv.classList.add('success');
                } else {
                    responseDiv.innerHTML = '<span class="status-message error">Error:</span><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    responseDiv.classList.add('error');
                }
            } catch (error) {
                responseDiv.innerHTML = '<span class="status-message error">Network Error:</span> ' + error.message;
                responseDiv.classList.add('error');
                console.error('Fetch error:', error);
            }
        });
    </script>
</body>
</html>
"""
# pylint: enable=C0301

html_file_path = os.path.join(STATIC_DIR, "index.html")
# pylint: disable=W1514 # Specified encoding for security review
with open(html_file_path, "w", encoding="utf-8") as file_to_write:
    file_to_write.write(HTML_CONTENT)
# pylint: enable=W1514

app = FastAPI(
    title="Service 1 API",
    description="Service 1 with a modern UI that calls Service 2.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def read_root():
    """Returns a welcome message from Service 1."""
    return {"message": "Hello from Service 1!"}

@app.get("/call-service2")
def call_service2():
    """Calls Service 2 and returns its response."""
    service_2_url = os.getenv("SERVICE_2_URL", "http://service2:8002/")
    try:
        response = requests.get(service_2_url, timeout=5)
        response.raise_for_status()
        return {"service1": "Calling Service 2", "response": response.json()}
    except requests.exceptions.Timeout:
        return {"error": "Service 2 call timed out", "details": f"Could not reach {service_2_url} within 5 seconds."}, 504
    except requests.exceptions.ConnectionError:
        return {"error": "Service 2 connection error", "details": f"Could not connect to {service_2_url}. Is Service 2 running?"}, 503
    except requests.exceptions.HTTPError as exc: # Renamed 'e' to 'exc' to avoid conflict
        return {"error": f"Service 2 returned an HTTP error: {exc.response.status_code}", "details": exc.response.text}, exc.response.status_code
    except requests.exceptions.RequestException as exc: # Renamed 'e' to 'exc' to avoid conflict
        return {"error": str(exc)}, 500

@app.get("/ui", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    """Serves the Service 1 UI."""
    # pylint: disable=W1514,W0621 # Specified encoding; renamed file_handle for clarity
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as file_handle:
        return HTMLResponse(content=file_handle.read())
    # pylint: enable=W1514,W0621

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static_assets")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)