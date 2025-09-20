import os
import select
import threading
import time
import subprocess

def show_fds():
    pid = os.getpid()
    cmd = f"lsof -p {pid} | awk '{{print $5}}' | sort | uniq -c | sort -nr"
    out = subprocess.check_output(cmd, shell=True)
    print(out.decode())


def create_epoll():
    # 创建 epoll 对象但不 close -> 泄露 epoll fd
    # epolls = []
    ep = select.epoll()   # <- 这是会在内核分配一个 fd 的地方
    # 不注册也会占 fd，若不关闭则泄露
    return ep

if __name__ == "__main__":
    print("初始 FD：")
    show_fds()

    threads = []
    results = []
    for _ in range(6):
        t = threading.Thread(target=lambda lst: lst.append(create_epoll()), args=(results,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    time.sleep(0.2)
    print("\n创建 epoll 对象 之后：")
    show_fds()