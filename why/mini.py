import os
import threading
import time
import subprocess

import sentry_sdk
import requests



def send_log():
    requests.get("https://www.baidu.com")
    print("send_log done")

def show_fds():
    pid = os.getpid()
    cmd = f"lsof -p {pid} | awk '{{print $5}}' | sort | uniq -c | sort -nr"
    out = subprocess.check_output(cmd, shell=True)
    print(out.decode())


if __name__ == "__main__":
    print("初始 FD：")
    show_fds()

    # 多线程触发
    threads = [threading.Thread(target=send_log) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    time.sleep(1)
    print("\n触发请求后 FD：")
    show_fds()
