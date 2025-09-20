import os
import subprocess
import threading
import selectors
import time


def show_fds():
    pid = os.getpid()
    cmd = f"lsof -p {pid} | awk '{{print $5}}' | sort | uniq -c | sort -nr"
    out = subprocess.check_output(cmd, shell=True)
    print(out.decode())

def create_epoll():
    sel = selectors.DefaultSelector()
    # 这里不关闭
    # sel.close()

if __name__ == "__main__":
    print("初始 FD：")
    show_fds()

    threads = [threading.Thread(target=create_epoll) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    time.sleep(0.5)
    print("\n触发请求后 FD：")
    show_fds()