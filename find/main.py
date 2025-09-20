from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time


app = FastAPI()


def generate_stream():
    for i in range(3):
        yield f"{i}\n"
        time.sleep(1)


@app.get("/")
def stream_text():
    return StreamingResponse(generate_stream(), media_type="text/plain")
