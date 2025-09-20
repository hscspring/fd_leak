import requests
import threading
import time

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=2, pool_maxsize=2)
session.mount("http://", adapter)
session.mount("https://", adapter)

url = "http://localhost:8022"

def make_leak(i):
    try:
        print(f"[Thread-{i}] start")
        resp = requests.get(url, stream=True)
        for line in resp.iter_lines():
            print(f"[Thread-{i}] line: {line}")
            if b"2" in line:
                # 模拟异常中断，连接不释放
                raise Exception("simulate disconnect")
    except Exception as e:
        print(f"[Thread-{i}] Exception: {e}")

threads = []
for i in range(100):  # 数量较大，超过系统限制
    t = threading.Thread(target=make_leak, args=(i,))
    t.start()
    time.sleep(.3)
    threads.append(t)

for t in threads:
    t.join()
