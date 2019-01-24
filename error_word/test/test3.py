import threading


def run(n):
    print("run the thread: %s" % n)


def all_finished(threads):
    for th in threads:
        if th.isAlive():
            return False
    return True


if __name__ == '__main__':

    con = threading.Condition()
    threads = []
    for i in range(10):
        t = threading.Thread(target=run, args=(i,))
        t.start()
        threads.append(t)
        if len(threads) == 3:
            con.acquire()
            con.wait_for(all_finished)
            threads.clear()
            con.release()
    con.acquire()
    con.wait_for(all_finished(threads))
    con.release()
    print("主线程完毕")
