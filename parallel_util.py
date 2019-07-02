from threading import Thread

def parallelize(ta):
    threads = [Thread(target=target, args=args) for target, args in ta]
    #map(lambda t: t.start(), threads)
    #map(lambda t: t.join(),  threads)
    for t in threads: t.start()
    for t in threads: t.join()
