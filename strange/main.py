from threading import Thread
import queue

from fastapi import HTTPException, FastAPI
from fastapi.responses import StreamingResponse
import sentry_sdk
import requests


session = requests.Session()

def send_log():
    resp = session.get("https://www.baidu.com")
    print(f"send log success.")



class Worker:
    def __init__(self):
        sentry_sdk.init(
            dsn="http://example@sentry.io/1",
            auto_enabling_integrations=False
        )
        self.input_queue = queue.Queue()

        def worker():
            while True:
                q, response_queue = self.input_queue.get()
                if q is None:
                    break
                for i in range(3):
                    token = f"token-{i}"
                    response_queue.put(token)
                response_queue.put(None)
        Thread(target=worker).start()
    
    
    def run(self, q: str):
        response_queue = queue.Queue()
        self.input_queue.put((q, response_queue))
        
        while True:
            token = response_queue.get()
            if token is None:
                break
            yield f"data: {token}\n\n"
        
        Thread(
            target=send_log,
            args=(),
        ).start()


worker = Worker()

app = FastAPI()


@app.post("/", response_model=None)
def llm_svc(q: str):
    return StreamingResponse(
        worker.run(q), 
        media_type="text/event-stream", 
    )


# lsof -p $(ps aux|grep uvicorn |grep 9321 | awk '{print $2}') | awk '{print $5}' | sort | uniq -c | sort -nr