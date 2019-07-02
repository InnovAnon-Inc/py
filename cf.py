#import array
#import random

from os         import devnull
from os         import environ
from os         import listdir
from os         import mkdir
from os         import remove
from os         import sep
from os         import walk
from os.path    import exists
from os.path    import isdir
from os.path    import join
from random     import choice
from shutil     import copyfileobj
from shutil     import copytree
from shutil     import rmtree
from subprocess import CalledProcessError
from subprocess import DEVNULL
from subprocess import PIPE
from subprocess import Popen
from subprocess import check_call
from sys        import stdout
from tempfile   import mkdtemp
from timeit     import timeit
from threading  import Thread

from SimpleGA   import SimpleGA

class CF(SimpleGA):
    def __init__(self):
        super().__init__('cf3.in')
        #self.srcdir, self.datadir = checkoutSource()
        home      = environ['HOME']
        self.allSrcdir = join(home,      'src')
        self.srcdir    = join(self.allSrcdir, 'xz')
        self.datadir   = join(home, 'data', 'xz')
    def generate_individual(self):
        result = super().generate_individual()

        genes1  = [prof, afdo, noprof]
        gene1   = choice(genes1)

        genes2  = [pack, nopack]
        gene2   = choice(genes2)

        #def wrapper(ws, srcdir, datadir, myEnv):
        #    gene1(ws, srcdir, datadir, myEnv)
        #    gene2(ws, srcdir, datadir, myEnv)
        #return   wrapper, result
        return gene1, gene2, result
    def evalOneMax(self, fIndividual):
        gene1, gene2, individual = fIndividual

        ws = mkdtemp()
        myEnv = setupEnv(ws, individual)
        try:
            #addFlagsToEnv(myEnv, 'CFLAGS', ['-fprofile-dir=%s/pgo' % ws])
            print("specimen            : %s" % fIndividual)
            #print("specimen            : %s" % individual)
            gene1(ws, self.srcdir, self.datadir, myEnv)
            gene2(ws, self.srcdir, self.datadir, myEnv)

            rt = timeit(lambda: run_benchmark    (ws, self.datadir, myEnv), number=30)
            print("run benchmark      : %s" % rt)
            return -rt,
        except CalledProcessError as e:
            print(e)
            return -float("inf"),
        finally: rmtree(ws)

def checkoutSource(home, allSrcdir, srcdir):
    #home      = environ['HOME']
    #allSrcdir = join(home,      'src')
    #srcdir    = join(allSrcdir, 'xz')
    # TODO env ?
    #if not isdir(srcdir): check_call(['git', 'clone', 'https://git.tukaani.org/xz.git'], cwd=allSrcdir, stdout=DEVNULL, stderr=DEVNULL)
    #else:                 check_call(['git', 'reset', '--hard'],                         cwd=srcdir,    stdout=DEVNULL, stderr=DEVNULL)
    #assert isdir(srcdir)
    #check_call([join('.', 'autogen.sh')], cwd=srcdir, stdout=DEVNULL, stderr=DEVNULL)
    #assert exists(join(srcdir, 'configure'))
    #return srcdir, join(home, 'data', 'xz')
    if not isdir(srcdir): check_call(['git', 'clone', 'https://git.tukaani.org/xz.git'], cwd=allSrcdir, stdout=DEVNULL, stderr=DEVNULL)
    else:                 check_call(['git', 'reset', '--hard'],                         cwd=srcdir,    stdout=DEVNULL, stderr=DEVNULL)
    assert isdir(srcdir)
    check_call([join('.', 'autogen.sh')], cwd=srcdir, stdout=DEVNULL, stderr=DEVNULL)
    assert exists(join(srcdir, 'configure'))

def pack(ws, srcdir, datadir, myEnv):
    for exe in ['xz']:
        #('lzcmp', 'lzgrep', 'lzmainfo',
        #'xz', 'xzdiff', 'xzless',
        #'lzdiff', 'lzless', 'lzmore',
        #'xzcat', 'xzegrep', 'xzmore',
        #'lzegrep', 'lzma', 'unlzma',
        #'xzcmp', 'xzfgrep',
        #'lzcat', 'lzfgrep', 'lzmadec',
        #'unxz', 'xzdec', 'xzgrep'):
        try: check_call(['upx', '-all-filters', '--ultra-brute', join(ws, 'bin', exe)], stdout=DEVNULL, stderr=DEVNULL)
        except CalledProcessError: pass
def nopack(ws, srcdir, datadir, myEnv): pass

def noprof(ws, srcdir, datadir, myEnv):
    rt = timeit(lambda: compileSource2   (ws, srcdir,  myEnv), number=1)
    print("compile source 2    : %s" % rt)

def prof(ws, srcdir, datadir, myEnv):
    rt = timeit(lambda: compileSource    (ws, srcdir,  myEnv), number=1)
    print("compile source 1    : %s" % rt)
            
    rt = timeit(lambda: run_benchmark    (ws, datadir, myEnv), number=1)
    print("run PGO training set: %s" % rt)
    assert isdir(join(ws, 'fbdata.prof'))
    map(print, listdir(join(ws, 'fbdata.prof')))

    rt = timeit(lambda: recompileSource  (ws, srcdir,  myEnv), number=1)
    print("recompile source 1  : %s" % rt)
    assert not isdir(join(ws, 'fbdata.prof'))

def afdo(ws, srcdir, datadir, myEnv):
    rt = timeit(lambda: compileSource2   (ws, srcdir,  myEnv), number=1)
    print("compile source 2    : %s" % rt)

    rt = timeit(lambda: runPerfCov       (ws, datadir, myEnv), number=1)
    print("run perf and gcov   : %s" % rt)
    assert exists(join(ws, 'fbdata.afdo'))

    rt = timeit(lambda: recompileSource2 (ws, srcdir,  myEnv), number=1)
    print("recompile source 2  : %s" % rt)
    assert not exists(join(ws, 'fbdata.afdo'))

def compileSourceHelper(ws, srcdir, myEnv, cflag, chk, verbose):
    mySrcdir = join(ws, 'src')
    myEnv = dict(myEnv)
    addFlagsToEnv(myEnv, 'CFLAGS', cflag)
    mkdir(mySrcdir)
    #chdir(mySrcdir)
    #try:
    try:
        if verbose: check_call([join(srcdir, 'configure'), '--prefix=%s' % ws], cwd=mySrcdir, env=myEnv)#, stdout=DEVNULL, stderr=DEVNULL)
        else:       check_call([join(srcdir, 'configure'), '--prefix=%s' % ws], cwd=mySrcdir, env=myEnv, stdout=DEVNULL, stderr=DEVNULL)
    except CalledProcessError as e:
        #with open(join(mySrcdir, 'config.log'), 'r') as cl: copyfileobj(cl, stdout)
        raise e
    #check_call([join(srcdir, 'configure'), '--prefix=%s' % ws], cwd=mySrcdir, env=myEnv)#, stdout=DEVNULL, stderr=DEVNULL)
    assert exists(join(mySrcdir, 'Makefile'))
    check_call(['make'],                                      cwd=mySrcdir, env=myEnv, stdout=DEVNULL, stderr=DEVNULL)
    if chk: check_call(['make', 'check'], cwd=mySrcdir, env=myEnv, stdout=DEVNULL, stderr=DEVNULL)
    # TODO create binary package and install
    check_call(['make', 'install'],                           cwd=mySrcdir, env=myEnv, stdout=DEVNULL, stderr=DEVNULL)
    assert exists(join(ws, 'bin', 'xz'))
    #finally: chdir(ws)
    #check_call(['make', 'installcheck'],                      cwd=mySrcdir, env=myEnv, stdout=DEVNULL, stderr=DEVNULL)

def compileSource(ws, srcdir, myEnv): compileSourceHelper(ws, srcdir, myEnv,
    ['-fprofile-generate=%s' % join(ws, 'fbdata.prof')], True, False)

def compileSource2(ws, srcdir, myEnv): compileSourceHelper(ws, srcdir, myEnv,
    [], True, False)

def recompileSource(ws, srcdir, myEnv):
    mySrcdir = join(ws, 'src')
    rmtree(mySrcdir)
    #compileSourceHelper(ws, srcdir, myEnv, ['-fprofile-use=%s' % join(ws, 'fbdata.prof'), '-fprofile-correction'], False, True)
    compileSourceHelper(ws, srcdir, myEnv, ['-fprofile-use=%s' % join(ws, 'fbdata.prof'), '-fprofile-correction'], False, False)
    rmtree(join(ws, 'fbdata.prof'))

def recompileSource2(ws, srcdir, myEnv):
    mySrcdir = join(ws, 'src')
    rmtree(mySrcdir)
    #compileSourceHelper(ws, srcdir, myEnv, ['-fauto-profile=%s' % join(ws, 'fbdata.afdo')], False, True)
    compileSourceHelper(ws, srcdir, myEnv, ['-fauto-profile=%s' % join(ws, 'fbdata.afdo')], False, False)
    remove(join(ws, 'fbdata.afdo'))

def runBenchmarkHelper(ws, datadir, myEnv, f1, f2):
    xz = "xz"

    #out = join(ws, "data.txz")
    myDataDir = join(ws, 'data')

    mkdir(myDataDir)

    tar   = Popen(['tar', '-cf-', '.'], cwd=datadir, stdin=DEVNULL,    stdout=PIPE)#,    stderr=DEVNULL)
    z     = Popen([xz, '-9e'],          env=myEnv,   stdin=tar.stdout, stdout=PIPE)#,    stderr=DEVNULL)
    unz   = Popen([xz, '-d'],           env=myEnv,   stdin=z.stdout,   stdout=PIPE)#,    stderr=DEVNULL)
    untar = Popen(['tar', '-xC', myDataDir],                stdin=unz.stdout)#, stdout=DEVNULL)#, stderr=DEVNULL)

    result = f1(z.pid, unz.pid)

    tar.stdout.close()
    tar.stdout = None

    z.stdout.close()
    z.stdout   = None

    unz.stdout.close()
    unz.stdout = None

    Thread(target=tar.communicate, args=[]).start()
    Thread(target=z.communicate,   args=[]).start()
    Thread(target=unz.communicate, args=[]).start()

    untar.communicate()
    #remove(out)

    f2(result)

    rmtree(myDataDir)

    # TODO <home>/data/xz and <ws>/data

def runPerfCov(ws, datadir, myEnv):
    def f1(pid1, pid2): return Popen(['perf', 'record',
        '-e', 'cpu/event=0xc4,umask=0x20,name=br_inst_retired_near_taken,period=400009/pp',
        '-p', ','.join([str(pid1), str(pid2)]),
        '-b',
        '-o', join(ws, 'perf.data')])
    def f2(perf):
        perf.communicate()
        check_call(['create_gcov',
            '--binary=%s'  % join(ws, 'bin', 'xz'),
            '--profile=%s' % join(ws, 'perf.data'),
            '--gcov=%s'    % join(ws, 'fbdata.afdo'),
            '--gcov_version', str(1)])
        remove(join(ws, 'perf.data'))
    runBenchmarkHelper(ws, datadir, myEnv, f1, f2)

def run_benchmark(ws, datadir, myEnv):
    def f1(pid1, pid2): return None
    def f2(result):     pass
    runBenchmarkHelper(ws, datadir, myEnv, f1, f2)

def setupEnv(ws, cflags):
    myEnv = {}
    addPathToEnv(myEnv, 'LD_LIBRARY_PATH', ws, 'lib')
    addPathToEnv(myEnv, 'LIBRARY_PATH',    ws, 'lib')
    addPathToEnv(myEnv, 'LD_RUN_PATH',     ws, 'lib')
    #addPathToEnv(myEnv, 'C_PATH',           ws, 'include')
    addPathToEnv(myEnv, 'CPATH',           ws, 'include')
    addPathToEnv(myEnv, 'PATH',            ws, 'bin')
    # TODO portable file separator
    addPathToEnv(myEnv, 'PKG_CONFIG_PATH', ws, join('lib', 'pkgconfig'))
    addFlagsToEnv(myEnv, 'CFLAGS',         cflags)
    return myEnv
def addPathToEnv(d, varname, base, path): d[varname] = prepend_path(varname, base, path)
def prepend_path(varname, base, path):
    k      = environ.get(varname, None)
    myPath = join(base, path)
    return ":".join([myPath, k]) if k else myPath
def addFlagsToEnv(d, varname, flags): d[varname] = append_flags(varname, flags)
def append_flags(varname, flags):
    var = environ.get(varname, None)
    return ' '.join([var] + flags) if var else ' '.join(flags)

def main():
    home      = environ['HOME']
    allSrcdir = join(home,      'src')
    srcdir    = join(allSrcdir, 'xz')
    checkoutSource(home, allSrcdir, srcdir)

    ga = CF()
    ga.setupGA()
    pop, log, hof = ga.runGA()
    # TODO create binary distribution
    return hof

if __name__ == "__main__":
    main()

