from hashlib            import md5
from multiprocessing    import Pool
from os.path            import basename
from os.path            import exists
from os.path            import join
from timeit             import timeit
from wget               import download

from download_util      import downloadIfNewer
from download_util      import pdownloadList
from hash_c             import pmd5_c_open
from parallel_util      import parallelize
from string_util        import chomp

def getLists(wgetList, md5sums, destdir):
    def getLines(l):
        downloadIfNewer(l, destdir)
        with open(join(destdir, basename(l)), 'r') as f: lines = f.readlines()
        return map(chomp, lines)
    wl, ml = {}, {}
    def urlHelper():
        for k in getLines(wgetList): wl[basename(k)] = k
    def md5Helper():
        for k, p in map(lambda s: s.split(), getLines(md5sums)): ml[p] = k
    parallelize([
        (urlHelper, []),
        (md5Helper, [])
    ])
    return wl, ml
def phash_c_download(wgetList, md5sums, destdir): return phash_c_download_helper(destdir, *getLists(wgetList, md5sums, destdir))
    
def phash_c_download_helper(destdir, wl, ml):
    #assert len(wl) is len(ml)
    #md5s, files = zip(*map(lambda s: s.split(), ml))

    # TODO combine files + wl_files

    #data = {}
    #for f in wl:
    #    url = wl[f]
    #    h   = ml.get(f, None)
    #    data[f] = (url, join(destdir, f), h)
    data = ((wl[f], join(destdir, f), ml.get(f, None)) for f in wl)

    p = Pool()
    try: return p.starmap(dlck, data)
    finally:
        p.close()
        p.join()
def dlck(url, fname, h):
    if not exists(fname):
        if url is None: return 1, 0, 0, 0
        download(url, fname)
    if h is None: return 0, 1, 0, 0
    m = md5()
    with open(fname, 'rb') as fd: fc = fd.read()
    m.update(fc)
    if h == m.hexdigest(): return 0, 0, 1, 0
    return 0, 0, 0, 1
    #return h == m.hexdigest()

def phash_c_download_stats(wgetList, md5sums, destdir): return map(sum, zip(*phash_c_download(wgetList, md5sums, destdir)))

def phash_c_download_old(wgetList, md5sums, destdir):
    parallelize([
        (pdownloadList,   [wgetList, destdir]),
        (downloadIfNewer, [md5sums,  destdir])
    ])
    return sum(pmd5_c_open(join(destdir, basename(md5sums)), destdir))

def main():
    domain   = 'http://www.linuxfromscratch.org/lfs/view/development'
    wgetList = '%s/wget-list' % domain
    md5sums  = '%s/md5sums'   % domain
    destdir  = join('.', 'sources')
    results = [None]
    #def foo(): results[0] = phash_c_download(wgetList, md5sums, destdir)
    def foo(): results[0] = phash_c_download_old(wgetList, md5sums, destdir)
    rt = timeit(foo, number=1)
    #results = results[0]
    #missing_urls, missing_hashes, correct_hashes, failed_hashes = results[0]
    #print(rt, missing_urls, missing_hashes, correct_hashes, failed_hashes)
    correct_hashes = results[0]
    print(rt, correct_hashes)
if __name__ == "__main__": main()
