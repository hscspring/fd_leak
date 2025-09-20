import requests


def call_service(q: str):  
    url = "http://127.0.0.1:9321/?q=q"
    response = requests.post(url, stream=True)
    for chunk in response.iter_lines():
        if chunk:
            yield chunk.decode("utf-8")


if __name__ == "__main__":    
    for i in range(10):
        gen = call_service("hello")
        for cont in gen:
            print(f"-->receive cont: {cont!r}")