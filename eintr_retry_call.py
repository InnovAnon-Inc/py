from errno import EINTR

""" https://stackoverflow.com/questions/30160211/python-subprocess-ioerror-errno-4 """
def _eintr_retry_call(func, *args):
    while True:
        try: return func(*args)
        except (OSError, IOError) as e:
            if e.errno == EINTR: continue
            raise
