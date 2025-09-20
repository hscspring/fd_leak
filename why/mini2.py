import os, sys
import threading
import time
import subprocess

# from eventlet.patcher import is_monkey_patched
# from eventlet import convenience
# from eventlet.green import socket
# from eventlet.support import greendns
# from eventlet import greenio
# eventlet.patcher
# from eventlet import patcher


import eventlet
# eventlet.monkey_patch()
# eventlet.monkey_patch(thread=True)
# from eventlet.patcher import is_monkey_patched

import urllib3


def send_log():
    try:
        urllib3.request("GET", "127.0.0.1")
    except Exception as e:
        pass


def show_fds():
    pid = os.getpid()
    cmd = f"lsof -p {pid} | awk '{{print $5}}' | sort | uniq -c | sort -nr"
    out = subprocess.check_output(cmd, shell=True)
    print(out.decode())
    cmd2 = f"lsof -p {pid} | grep a_inode"
    out2 = subprocess.check_output(cmd2, shell=True)
    print(out2.decode())


if __name__ == "__main__":
    print("初始 FD：")
    show_fds()

    # 多线程触发
    threads = [threading.Thread(target=send_log) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # time.sleep(1)
    print("\n触发请求后 FD：")
    show_fds()
