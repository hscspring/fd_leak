import threading

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import sentry_sdk
import requests

sentry_sdk.init(
    dsn="http://example@sentry.io/1",
    auto_enabling_integrations=False
)
session = requests.Session()


def send_log():
    resp = session.get("https://www.baidu.com")
    print(f"send log success.")


app = FastAPI()


@app.post("/")
def stream_tokens(q: str):
    def generator():
        for i in range(3):
            yield f"data: token-{i}\n\n"
        # threading.Thread(target=send_log).start()
        send_log()
    return StreamingResponse(generator(), media_type="text/event-stream")


# lsof -p $(ps aux|grep uvicorn |grep 9321 | awk '{print $2}') | awk '{print $5}' | sort | uniq -c | sort -nr