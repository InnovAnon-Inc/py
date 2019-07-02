from itertools       import zip_longest
from multiprocessing import Pool
from os.path         import basename
from os.path         import exists
from os.path         import join
from urllib.error    import HTTPError
from wget            import download

from string_util     import chomp

""" https://stackabuse.com/download-files-with-python/ """
def downloadURL(url, destdir):
    #headers = {'user-agent': 'test-app/0.0.1'}
    #r = get(url, headers=headers)

    #fname = LFS.chomp(basename(url))
    #fname = basename(url)
    #fname = join(destdir, fname)
    fname = downloadURLHelper(url, destdir)

    #with open(fname, 'wb') as f: f.write(r.content)

    # Retrieve HTTP meta-data
    #print(r.status_code)
    #print(r.headers['content-type'])
    #print(r.encoding)
    if exists(fname): return
    try:              download(url, fname)
    except HTTPError: pass

def downloadIfNewer(url, destdir):
    fname = downloadURLHelper(url, destdir)
    #fname = basename(url)
    # TODO check timestamps
    #fname = join(destdir, fname)
    if exists(fname): return
    downloadURL(url, destdir)

def downloadURLHelper(url, destdir): return join(destdir, basename(url))
def downloadURLsHelper(l):
    with open(l) as w: return map(chomp, w.readlines())
def downloadURLs(l, destdir):
    urls = downloadURLsHelper(l)
    #for url in urls:
    #    fname = downloadURLHelper(url)
    #    downloadURL(url, fname)
    for url in urls: downloadURL(url, destdir)
def downloadListHelper(url, f, destdir):
    #fname = downloadURLHelper(url, destdir)
    #downloadIfNewer(url, fname)
    downloadIfNewer(url, destdir)
    #fname = basename(url)
    #fname = basename(url)
    #fname = join(destdir, fname)
    #fname = downloadURLHelper(url, destdir)
    fname = downloadURLHelper(url, destdir)
    #l = downloadURLsHelper(fname)
    f(fname, destdir)
def downloadList(url, destdir): downloadListHelper(url, downloadURLs, destdir)

def pdownloadURLs(l, destdir):
    urls = downloadURLsHelper(l)
    #fnames = (downloadURLHelper(url, destdir) for url in urls)
    # TODO select a reasonable number of threads for the total download rate vs max download bandwidth
    p = Pool()
    p.starmap(downloadURL, zip_longest(urls, [], fillvalue=destdir))
    #p.map(lambda u: downloadURL(u, destdir), urls)
    p.close()
    p.join()
def pdownloadList(url, destdir): downloadListHelper(url, pdownloadURLs, destdir)

def main():
    url   = "https://i.stack.imgur.com/PKRRF.jpg"
    fname = basename(url)
    if exists(fname): raise Error()
    download(url)
    assert exists(fname)
if __name__ == "__main__": main()
