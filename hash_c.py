from itertools import zip_longest
from hashlib import md5
from multiprocessing import Pool
from os.path import join

def pmd5_c_open(md5sums, destdir): return phash_c_open(md5sums, md5, destdir)
def md5_c_open(md5sums, destdir): return hash_c_open(md5sums, md5, destdir)

def hash_c_open_helper(md5sums, h, destdir, f):
    with open(md5sums, 'r') as m: l = m.readlines()
    md5s = (s.split() for s in l)
    return f(md5s, h, destdir)
def phash_c_open(md5sums, h, destdir): return hash_c_open_helper(
    md5sums, h, destdir, phash_c)
def hash_c_open(md5sums, h, destdir): return hash_c_open_helper(
    md5sums, h, destdir, hash_c)

def hash_helper(md5, f, h, destdir):
    m = h()
    f = join(destdir, f)
    with open(f, 'rb') as fd: fc = fd.read()
    m.update(fc)
    return md5 == m.hexdigest()

def hash_c(md5s, h, destdir): return sum((bool(hash_helper(md5, f, h, destdir)) for md5, f in md5s))
    #cnt = 0
    #for md5, f in md5s:
    #    if hash_helper(md5, f, h, destdir): cnt = cnt + 1
    #return cnt
def phash_c(md5s, h, destdir):
    p = Pool()
    try: return p.starmap(hash_helper, map(lambda m: (m[0], m[1], h, destdir), md5s))
    finally:
        p.close()
        p.join()

