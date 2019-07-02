from abc             import ABC
from abc             import abstractmethod

from traceback      import format_exc
from multiprocessing import cpu_count
from threading       import Thread
from os              import chdir
import os
#from os              import environ
from os              import getcwd
from os              import getuid
from os              import makedirs
from os              import mkdir
from os              import remove
from os              import rmdir
from os              import sep
from os              import symlink
from subprocess      import DEVNULL
from os.path         import dirname
from os.path         import exists
from os.path         import expanduser
from os.path         import isdir
from os.path         import join
from platform        import uname
from pwd             import getpwnam
from shutil          import chown
from shutil          import copyfile
from shutil          import copytree
from shutil          import rmtree
from subprocess      import check_call
from tempfile        import mkdtemp
from tarfile         import open as topen

from chmod_util       import chmod_a_plus_wt
from disk_util        import toBytes
from string_util      import chomp
from drop_privileges  import dropChildPrivileges
from LFSAbs           import LFSAbs
from parallel_util    import parallelize
from eintr_retry_call import _eintr_retry_call
from phash_c_download import phash_c_download_stats

from lfs_util import createRamdisk
from lfs_util import removeRamdisk
from lfs_util import makeflagFormula

class ToolsChild(LFSAbs):
    def __init__(self, lfstools):
        self.lfstools = lfstools
        self.pathdir = lfstools.pathdir
        self.path    = lfstools.path
        self.fstype  = lfstools.fstype
        self.lfs     = lfstools.lfs
        self.sz      = lfstools.sz
        self.lo      = lfstools.lo
        self.tools   = lfstools.tools
        self.toolsym = lfstools.toolsym
        self.sources = lfstools.sources
        self.cpsrc   = lfstools.cpsrc
        self.srcx    = lfstools.srcx
        self.lfs_dns = lfstools.lfs_dns
        self.group   = lfstools.group
        self.user    = lfstools.user
        self.lfs_tgt = lfstools.lfs_tgt

    def buildDistro(self):
        print("build distro")
        self.setupEnvironment()
        self.aboutSBUs()
        self.constructTemporarySystem()
    """ II 4.4 """
    def setupEnvironment(self):
        print("setup environment")
        home = _eintr_retry_call(getpwnam, self.user).pw_dir
        def cp(x): _eintr_retry_call(copyfile, x, join(home, x))
        #t1 = Thread(target=cp, args=[".bash_profile"])
        #t2 = Thread(target=cp, args=[".bashrc"])
        #t1.start()
        #t2.start()
        #t1.join()
        #t2.join()
        def sed(x):
            with open(x, 'r') as f: s = f.read()
            s.replace('/mnt/lfs', self.lfs)
            s.replace('LFS_TGT=$(uname -m)-lfs-linux-gnu', self.lfs_tgt)
            with open(join(home, x), 'w') as f: f.write(s)
        parallelize([
            (sed, [".bash_profile"]),
            # TODO sed /mnt/lfs with self.lfs 
            (cp,  [".bashrc"])
        ])

        """ https://stackoverflow.com/questions/8365394/set-environment-variable-in-python-script#8365493 """
        term = os.environ['TERM']
        os.environ = { 'HOME' : home, 'TERM' : term, 'PS1' : """\\u:\\w\\$ """}
        
        #copyfile('.bash_profile', expanduser("~/.bash_profile"))
        #copyfile('.bashrc',       expanduser("~/.bashrc"))
        # TODO lfs handbook really wants us to exec env (the latter also does an exec)
        #exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash
    """ II 4.5 """
    """ https://stackoverflow.com/questions/1006289/how-to-find-out-the-number-of-cpus-using-python#1006337 """
    def aboutSBUs(self):
        print("about SBUs")
        os.environ['MAKEFLAGS'] = "-j%s" % makeflagFormula(cpu_count())

    """ II 5 """
    def constructTemporarySystem(self):
        print("construct temporary system")
        self.compileBinutils1()
        self.compileGcc1()
        self.compileLinuxHeaders()
        self.compileGlibc()
        self.compileLibstdcpp()
        self.compileBinutils2()
        self.compileGcc2()
        self.compileTcl()
        self.compileExpect()
        self.compileDejaGnu()
        self.compileM4()
        self.compileNcurses()
        self.compileBash()
        self.compileBison()
        self.compileBzip2()
        self.compileCoreutils()
        self.compileDiffutils()
        self.compileFile()
        self.compileFindutils()
        self.compileGawk()
        self.compileGettext()
        self.compileGrep()
        self.compileGzip()
        self.compileMake()
        self.compilePatch()
        self.compilePerl()
        self.compilePython()
        self.compileSed()
        self.compileTar()
        self.compileTexinfo()
        self.compileXz()
        self.strip()
        self.changeOwnership()

    """ II 5.3 """
    def compilePackage(self, name, version, fmt, s, arc, build):
        print("lfs compile package")

        #pkgd    = '%s-%s' % (name, version)
        #pkg     = '%s.%s' % (pkgd, fmt)
        #arc     = join(self.sources, pkg)
        #s       = join(self.srcx, pkgd)
        d       = mkdtemp(dir=self.srcx)

        #with tarfile.open(pkg, 'r') as tar: tar.extractall(self.srcx)
        #s = mkdtemp(dir=self.srcx)
        #print("made temp source dir: %s" % s)
        try:
            with topen(arc, 'r') as tar: tar.extractall(self.srcx)

            #d = join(self.srcx, 'build')
            #mkdir(d)

            #chdir(d)

            build(d)
        finally:
            #chdir(self.srcx)
            rmtree(d)
            rmtree(s)
    def buildHelper(self, s, d, preconf, configure, preinstall):
        print("build helper")
        preconf(d)
        check_call([join(s, 'configure')] + configure, cwd=d)
        check_call(['make'], cwd=d)
        preinstall(d)
        check_call(['make', 'install'], cwd=d)        
       

    def compileBinutils1(self):
        print("compile binutils (pass 1)")
        try:
            print("calling compile binutils 1 constructor")
            c = CompileBinutils1(self)
            print("finna compile binutils package")
            c.compilePackage()
            print("compiled binutils package")
        except:
            format_exc()
            raise Exception()
    def compileGcc1(self):
        print("compile gcc (pass 1)")
        c = CompileGcc1(self)
        c.compilePackage()

class Compile(ABC):
    def __init__(self, name, version, fmt, lfs):
        self.name    = name
        self.version = version
        self.fmt     = fmt
        self.lfs     = lfs

        self.pkgd    = '%s-%s' % (name, version)
        self.pkg     = '%s.%s' % (self.pkgd, fmt)
        self.arc     = join(lfs.sources, self.pkg)
        self.s       = join(lfs.srcx, self.pkgd)
    @abstractmethod
    def preconf(self, d): print("preconf")
    @abstractmethod
    def preinstall(self, d): print("preinstall")
    def compilePackage(self):
        print("my compile package")
        try:
            self.lfs.compilePackage(self.name, self.version, self.fmt,
                self.s, self.arc,
                lambda d: self.lfs.buildHelper(self.s, d,
                    self.preconf,
                    self.configure,
                    self.preinstall))
        except: format_exc()
class CompileBinutils1(Compile):
    #name    = 'binutils'
    #version = '2.32'
    #fmt     = 'tar.xz'
    #def __init__(self, lfs): self.lfs = lfs
    def __init__(self, lfs):
        print("init compile binutils 1")
        super().__init__('binutils', '2.32', 'tar.xz', lfs)
        print("called super constructor")
        self.configure = ['--prefix=%s' % lfs.toolsym, '--with-sysroot=%s' % lfs.lfs, '--with-lib-path=%s' % join(lfs.toolsym, 'lib'), '--target=%s' % lfs.lfs_tgt, '--disable-nls', '--disable-werror']
        print("leaving constructor")
    def preinstall(self, d):
        print("preinstall")
        if uname()[4] in 'x86_64':
            # TODO parallel
            mkdir(join(self.lfs.toolsym, 'lib'))
            symlink('lib', join(self.lfs.toolsym, 'lib64'))
    #def compilePackage(self):
    #    print("my compile package")
    #    self.lfs.compilePackage(self.name, self.version, self.fmt,
    #        lambda s, d: self.lfs.buildHelper(s, d,
    #            self.preconf,
    #            ['--prefix=%s' % self.lfs.toolsym, '--with-sysroot=%s' % self.lfs.lfs, '--with-lib-path=%s' % join(self.lfs.toolsym, 'lib'), '--target=%s' % self.lfs.lfs_tgt, '--disable-nls', '--disable-werror'],
    #            self.preinstall))
class CompileGcc1(Compile):
    def __init__(self, lfs):
        super().__init__('gcc', '9.1.0', 'tar.xz', lfs)
        # TODO
        self.configure = []
    def preconf(self, s, d):
        print("preconf")
        mpfr = CompileMPFR(self.lfs)
        mpc  = CompileMPC(self.lfs)
        gmp  = CompileGMP(self.lfs)
        # TODO parallel
        with topen(mpfr.arc, 'r') as tar: tar.extractall(s)
        mv(mpfr.s, 'mpfr')
        with topen(mpc.arc,  'r') as tar: tar.extractall(s)
        mv(mpc.s,  'mpc')
        with topen(gmp.arc,  'r') as tar: tar.extractall(s)
        mv(gmp.s,  'gmp')

        for file in map(lambda s: 'gcc/config/%slinux%s.h' % s, [('', ''),('i386/', ''),('i386/', '64')]):
            with open(file, 'r') as f: r = f.read()
            r = sub('/lib\(64\)\?\(32\)\?/ld', '/tools&', r)
            r = r.replace('/usr', '/tools')
#undef STANDARD_STARTFILE_PREFIX_1
#undef STANDARD_STARTFILE_PREFIX_2
#define STANDARD_STARTFILE_PREFIX_1 "%s"
#define STANDARD_STARTFILE_PREFIX_2 """"" % join(self.lfs.toolsym, 'lib')
            with open(file, 'w') as f: f.write(r)
            
        if uname()[4] in 'x86_64':
            with open('gcc/config/i386/t-linux64', 'r') as f: r = f.readlines()
            r = [l.replace('lib64', 'lib') if 'm64=' in l else l for l in r]
            with open('gcc/config/i386/t-linux64', 'w') as f: f.writelines(r)
class CompileMPFR(Compile):
    def __init__(self, lfs):
        super().__init__('mpfr', '4.0.2', 'tar.xz', lfs)
class CompileGMP(Compile):
    def __init__(self, lfs):
        super().__init__('gmp', '6.1.2', 'tar.xz', lfs)
class CompileMPC(Compile):
    def __init__(self, lfs):
        super().__init__('mpc', '1.1.0', 'tar.gz', lfs)
