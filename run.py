import uvicorn
import webbrowser
import threading
import time

def open_browser():
    # Delay to ensure server starts before browser tries to open it
    time.sleep(1)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    # Start a thread to open the browser
    threading.Thread(target=open_browser).start()

    # Run the FastAPI server
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
