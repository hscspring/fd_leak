#!/usr/bin/env python3
# leak_socket.py
import os
import socket
import threading
import time
import subprocess

def show_fds(tag=""):
    pid = os.getpid()
    # 用 /proc/self/fd 也可以看
    n = len(os.listdir(f"/proc/{pid}/fd"))
    print(f"{tag} /proc/{pid}/fd count = {n}")
    # 更详细（可注释）
    # out = subprocess.check_output(f"lsof -p {pid} | awk '{{print $4}}' | sort | uniq -c | sort -nr", shell=True)
    # print(out.decode())

def create_socket_leak(n):
    sockets = []
    for i in range(n):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 不连接也会占 FD
        sockets.append(s)
    # 保持引用，不关闭 -> 泄露
    return sockets

if __name__ == "__main__":
    print("初始 FD：")
    show_fds("before")

    # 每个线程创建很多 sockets
    threads = []
    results = []
    for _ in range(8):
        t = threading.Thread(target=lambda lst: lst.append(create_socket_leak(200)), args=(results,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    time.sleep(0.2)
    print("\n创建 sockets 之后：")
    show_fds("after (sockets created)")

    # 防止脚本立刻退出，方便用 lsof/ls查看
    print("按 Enter 退出并关闭（回收）")
    input()
    # 如果脚本退出，Python 会自动 close fds when objects GC'd (but最好显式关闭)
