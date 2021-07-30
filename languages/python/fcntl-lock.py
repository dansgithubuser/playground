import fcntl
import random
import threading
import time

def thread_main(thread_i):
    for i in range(10):
        lock = open('lock', 'w')
        fcntl.lockf(lock, fcntl.LOCK_EX)
        print(f'thread {thread_i}, iteration {i}, locked')
        time.sleep(random.random())
        print(f'thread {thread_i}, iteration {i}, unlocking')
        lock.close()

threads = []
for i in range(10):
    thread = threading.Thread(target=thread_main, args=(i,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
