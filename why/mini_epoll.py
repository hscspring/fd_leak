# epoll_only_leak.py
import threading
import select
import time
import os
import subprocess
import traceback

def show_fds():
    pid = os.getpid()
    try:
        out = subprocess.check_output(f"lsof -p {pid} | awk '{{print $5}}' | sort | uniq -c | sort -nr", shell=True)
        print(out.decode().strip())
    except Exception:
        fds = os.listdir(f"/proc/{pid}/fd")
        print("fd count:", len(fds))
        try:
            links = subprocess.check_output(f"ls -l /proc/{pid}/fd", shell=True)
            print(links.decode().strip())
        except Exception:
            pass

def worker_create_epoll(idx, leaked_list):
    try:
        ep = select.epoll()
    except AttributeError:
        print("epoll not supported on this platform")
        return

    print(f"[T{idx}] created epoll fd={ep.fileno()}")
    # traceback.print_stack(limit=5)

    # 故意不调用 ep.close()，把对象保存在列表里防止 GC -> 模拟泄露
    leaked_list.append(ep)

    # 保持短暂时间
    time.sleep(0.05)

if __name__ == "__main__":
    leaked = []

    print("初始 FD：")
    show_fds()

    threads = []
    for i in range(12):
        t = threading.Thread(target=worker_create_epoll, args=(i, leaked))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    time.sleep(0.2)
    print("\n触发后 FD：")
    show_fds()

    print("\n说明：如果在 worker 中执行 ep.close()，FD 将不会累积。")
