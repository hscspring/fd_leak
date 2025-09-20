# Server端不处理
import threading
import requests
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8022

def start_hang_server():
    class HangHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            # Server 端卡死
            time.sleep(30)
    server = HTTPServer(("localhost", PORT), HangHandler)
    server.serve_forever()

threading.Thread(target=start_hang_server).start()
time.sleep(1)

session = requests.Session()
stop_flag = False
lock = threading.Lock()

def open_conn():
    global stop_flag
    try:
        resp = session.get(
            f"http://localhost:{PORT}",
            stream=True,
            timeout=10,
        )
        for v in resp.iter_lines():
            if v:
                print(f"Received: {v.decode('utf-8')}")
    except Exception as e:
        print(f"Got exception in thread: {e!r}")
        # 如果是 Errno 16，就能看到类似 Device or resource busy
        with lock:
            stop_flag = True

count = 0
threads = []
while True:
    if stop_flag:
        print("Encountered failure, exiting loop.")
        break
    t = threading.Thread(target=open_conn)
    t.daemon = True
    t.start()
    threads.append(t)
    count += 1
    print(f"Opened connections: {count}")
    time.sleep(0.1)


for t in threads:
    t.join()