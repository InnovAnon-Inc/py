from abc             import ABC
from abc             import abstractmethod

from shutil         import move
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
from os             import listdir
from os             import unlink
from os             import umask
from os              import symlink
from sys               import stdout
from subprocess     import check_output
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
from re             import sub

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
        # TODO
        try:
            self.setupEnvironment()
            self.aboutSBUs()
            self.constructTemporarySystem()
        except: print(format_exc())
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
        os.environ = { 'HOME' : home, 'TERM' : term, 'PS1' : """\\u:\\w\\$ """,
                        'LFS' : self.lfs,
                        'LC_ALL' : 'POSIX',
                        'LFS_TGT' : '%s-lfs-linux-gnu' % uname()[4],
                        'PATH' : ':'.join([join(self.toolsym, 'bin'), join(sep, 'bin'), join(sep, 'usr', 'bin')])}
        
        umask(0o22)

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
        #self.compileBinutils1()
        #self.compileGcc1()
        #self.compileLinuxHeaders()
        self.compileGlibc()
        #self.compileLibstdcpp()
        #self.compileBinutils2()
        #self.compileGcc2()
        #self.compileTcl()
        #self.compileExpect()
        #self.compileDejaGnu()
        #self.compileM4()
        #self.compileNcurses()
        #self.compileBash()
        #self.compileBison()
        #self.compileBzip2()
        #self.compileCoreutils()
        #self.compileDiffutils()
        #self.compileFile()
        #self.compileFindutils()
        #self.compileGawk()
        #self.compileGettext()
        #self.compileGrep()
        #self.compileGzip()
        #self.compileMake()
        #self.compilePatch()
        #self.compilePerl()
        #self.compilePython()
        #self.compileSed()
        #self.compileTar()
        #self.compileTexinfo()
        #self.compileXz()
        #self.strip()
        #self.changeOwnership()

    """ II 5.3 """
    def compilePackage(self, name, version, fmt, s, arc, is_separate_builddir, build):
        print("lfs compile package")

        #pkgd    = '%s-%s' % (name, version)
        #pkg     = '%s.%s' % (pkgd, fmt)
        #arc     = join(self.sources, pkg)
        #s       = join(self.srcx, pkgd)
        if is_separate_builddir:
            #d       = mkdtemp(dir=self.srcx)
            d = join(s, 'build')
        else:
            d       = s

        #with tarfile.open(pkg, 'r') as tar: tar.extractall(self.srcx)
        #s = mkdtemp(dir=self.srcx)
        #print("made temp source dir: %s" % s)
        try:
            with topen(arc, 'r') as tar: tar.extractall(self.srcx)
            if is_separate_builddir:
                mkdir(d)

            #d = join(self.srcx, 'build')
            #mkdir(d)

            #chdir(d)

            build(d)
        #except: copyfile(join(d, 'config.log'), stdout)
        finally:
            #chdir(self.srcx)
            if is_separate_builddir:
                rmtree(d)
            rmtree(s)
    def buildHelper(self, s, d, preconf, configure, preinstall, postinstall):
        print("build helper")
        preconf(d)
        check_call([join(s, 'configure')] + configure(d), cwd=d)
        check_call(['make'], cwd=d)
        preinstall(d)
        check_call(['make', 'install'], cwd=d)
        postinstall(d)

    def compileBinutils1(self):
        print("compile binutils (pass 1)")
        #try:
        print("calling compile binutils 1 constructor")
        c = CompileBinutils1(self)
        print("finna compile binutils package")
        c.compilePackage()
        print("compiled binutils package")
        #except: print(format_exc())
            #raise Exception()
    def compileGcc1(self):
        print("compile gcc (pass 1)")
        c = CompileGcc1(self)
        c.compilePackage()
    def compileLinuxHeaders(self):
        c = CompileLinuxHeaders(self)
        c.compilePackage()
    def compileGlibc(self):
        c = CompileGlibc(self)
        c.compilePackage()
    def compileLibstdcpp(self):
        c = CompileLibstdcpp(self)
        c.compilePackage()
    def compileBinutils2(self):
        c = CompileBinutils2(self)
        c.compilePackage()










class Compile(ABC):
    def __init__(self, name, version, fmt, lfs, is_separate_builddir):
        print("in compile constructor")
        stdout.flush()
        self.name    = name
        self.version = version
        self.fmt     = fmt
        self.lfs     = lfs

        self.pkgd    = '%s-%s' % (name, version)
        self.pkg     = '%s.%s' % (self.pkgd, fmt)
        self.arc     = join(lfs.sources, self.pkg)
        self.s       = join(lfs.srcx, self.pkgd)

        self.is_separate_builddir = is_separate_builddir
    #@abstractmethod
    def preconf(self, d): print("preconf")
    #@abstractmethod
    def preinstall(self, d): print("preinstall")
    #@abstractmethod
    def postinstall(self, d): print("postinstall")
    def compilePackage(self):
        print("my compile package")
        #try:
        self.lfs.compilePackage(self.name, self.version, self.fmt,
            self.s, self.arc, self.is_separate_builddir,
            lambda d: self.lfs.buildHelper(self.s, d,
                self.preconf,
                self.configure,
                self.preinstall,
                self.postinstall))
        #except:
        #    # TODO
        #    print(format_exc())
class CompileBinutils1(Compile):
    #name    = 'binutils'
    #version = '2.32'
    #fmt     = 'tar.xz'
    #def __init__(self, lfs): self.lfs = lfs
    def __init__(self, lfs):
        print("init compile binutils 1")
        stdout.flush()
        super().__init__('binutils', '2.32', 'tar.xz', lfs, True)
        print("called super constructor")
        self.configure = lambda d: ['--prefix=%s' % lfs.toolsym, '--with-sysroot=%s' % lfs.lfs, '--with-lib-path=%s' % join(lfs.toolsym, 'lib'), '--target=%s' % lfs.lfs_tgt, '--disable-nls', '--disable-werror']
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
class CompileMPFR(Compile):
    def __init__(self, lfs):
        super().__init__('mpfr', '4.0.2', 'tar.xz', lfs, True)
class CompileGMP(Compile):
    def __init__(self, lfs):
        super().__init__('gmp', '6.1.2', 'tar.xz', lfs, True)
class CompileMPC(Compile):
    def __init__(self, lfs):
        super().__init__('mpc', '1.1.0', 'tar.gz', lfs, True)
class CompileGcc1(Compile):
    def __init__(self, lfs):
        super().__init__('gcc', '9.1.0', 'tar.xz', lfs, True)
        self.configure = lambda d: [
            '--target=%s' % self.lfs.lfs_tgt,
            '--prefix=%s' % self.lfs.toolsym,
            '--with-glibc-version=2.11',
            '--with-newlib',
            '--without-headers',
            '--with-local-prefix=%s' % self.lfs.toolsym,
            '--with-native-system-header-dir=%s' % join(self.lfs.toolsym, 'include'),
            '--disable-nls',
            '--disable-shared',
            '--disable-multilib',
            '--disable-decimal-float',
            '--disable-threads',
            '--disable-libatomic',
            '--disable-libgomp',
            '--disable-libquadmath',
            '--disable-libssp',
            '--disable-libvtv',
            '--disable-libstdcxx',
            '--enable-languages=c,c++']
    def preconf(self, d):
        print("preconf")
        mpfr = CompileMPFR(self.lfs)
        mpc  = CompileMPC(self.lfs)
        gmp  = CompileGMP(self.lfs)
        # TODO parallel
        with topen(mpfr.arc, 'r') as tar: tar.extractall(self.s)
        move(join(self.s, mpfr.pkgd), join(self.s, 'mpfr'))
        with topen(mpc.arc,  'r') as tar: tar.extractall(self.s)
        move(join(self.s, mpc.pkgd),  join(self.s, 'mpc'))
        with topen(gmp.arc,  'r') as tar: tar.extractall(self.s)
        move(join(self.s, gmp.pkgd),  join(self.s, 'gmp'))

        for file in map(lambda s: join(self.s, 'gcc/config/%slinux%s.h' % s), [('', ''),('i386/', ''),('i386/', '64')]):
            with open(file, 'r') as f: r = f.read()
            r = sub('/lib\(64\)\?\(32\)\?/ld', '/tools&', r)
            r = r.replace('/usr', '/tools')
#undef STANDARD_STARTFILE_PREFIX_1
#undef STANDARD_STARTFILE_PREFIX_2
#define STANDARD_STARTFILE_PREFIX_1 "%s"
#define STANDARD_STARTFILE_PREFIX_2 """"" % join(self.lfs.toolsym, 'lib')
            with open(file, 'w') as f: f.write(r)
            
        if uname()[4] in 'x86_64':
            with open(join(self.s, 'gcc/config/i386/t-linux64'), 'r') as f: r = f.readlines()
            r = [l.replace('lib64', 'lib') if 'm64=' in l else l for l in r]
            with open(join(self.s, 'gcc/config/i386/t-linux64'), 'w') as f: f.writelines(r)
class CompileLinuxHeaders(Compile):
    def __init__(self, lfs):
        super().__init__('linux', '5.1.15', 'tar.xz', lfs, False)
        def configure(d): pass
        self.configure = configure
    def compilePackage(self):
        print("my compile package")
        def buildHelper(d):
            check_call(['make', 'mrproper'], cwd=d)
            check_call(['make', 'INSTALL_HDR_PATH=dest', 'headers_install'], cwd=d)
            for f in listdir(join(d, 'dest', 'include')):
                move(join(d, 'dest', 'include', f), join(self.lfs.toolsym, 'include'))

        #try:
        self.lfs.compilePackage(self.name, self.version, self.fmt,
            self.s, self.arc, self.is_separate_builddir,
            lambda d: buildHelper(d))
        #except:
        #    # TODO
        #    print(format_exc())
class CompileGlibc(Compile):
    def __init__(self, lfs):
        super().__init__('glibc', '2.29', 'tar.xz', lfs, True)
        self.configure = lambda d: [
            '--prefix=%s' % self.lfs.toolsym,
            '--host=%s' % self.lfs.lfs_tgt,
            '--build=%s' % check_output([join(self.s, 'scripts/config.guess')], cwd=d)[:-1].decode(),
            '--enable-kernel=3.2',
            '--with-headers=%s' % join(self.lfs.toolsym, 'include')
        ]
    def postinstall(self, d):
        print(os.environ['PATH'])
        with open(join(d, 'dummy.c'), 'w') as f:
            f.write('int main(){}')
        check_call(['%s-gcc' % self.lfs.lfs_tgt, 'dummy.c'], cwd=d)
        o = check_output(['readelf', '-l', 'a.out'], cwd=d)
        if not ': /tools' in o: raise Exception()
        unlink(join(d, 'dummy.c'))
        unlink(join(d, 'a.out'))
class CompileLibstdcpp(Compile):
    def __init__ (self, lfs):
        super().__init__('gcc', '9.1.0', 'tar.xz', lfs, True)
        self.configure = lambda d: [
            '--host=%s' % self.lfs.lfs_tgt,
            '--prefix=%s' % self.lfs.toolsym,
            '--disable-multilib',
            '--disable-nls',
            '--disable-libstdcxx-threads',
            '--disable-libstdcxx-pch',
            '--with-gxx-include-dir=%s/include/c++/%s' % (join(self.lfs.toolsym, self.lfs.lfs_tgt), self.version)
        ]
    def preconf(self, d):
        print("preconf")
        mpfr = CompileMPFR(self.lfs)
        mpc  = CompileMPC(self.lfs)
        gmp  = CompileGMP(self.lfs)
        # TODO parallel
        with topen(mpfr.arc, 'r') as tar: tar.extractall(self.s)
        move(join(self.s, mpfr.pkgd), join(self.s, 'mpfr'))
        with topen(mpc.arc,  'r') as tar: tar.extractall(self.s)
        move(join(self.s, mpc.pkgd),  join(self.s, 'mpc'))
        with topen(gmp.arc,  'r') as tar: tar.extractall(self.s)
        move(join(self.s, gmp.pkgd),  join(self.s, 'gmp'))
class CompileBinutils2(Compile):
    def __init__(self, lfs):
        print("init compile binutils 2")
        super().__init__('binutils', '2.32', 'tar.xz', lfs, True)
        self.configure = lambda d: [
            '--prefix=%s' % lfs.toolsym,
            '--with-sysroot=%s' % lfs.lfs,
            '--with-lib-path=%s' % join(lfs.toolsym, 'lib'),
            '--target=%s' % lfs.lfs_tgt, '--disable-nls', '--disable-werror']
        print("leaving constructor")
    def compilePackage(self):
        print("my compile package")
        #try:
        def buildHelper(self, s, d, preconf, configure, preinstall, postinstall):
            print("build helper")
            preconf(d)
            myEnv = dict(os.environ, CC='%s-gcc' % self.lfs.lfs_tgt, AR='5s-ar' % self.lfs.lfs_tgt)
            check_call([join(s, 'configure')] + configure(d), cwd=d, env=myEnv)
            check_call(['make'], cwd=d)
            preinstall(d)
            check_call(['make', 'install'], cwd=d)
            postinstall(d)
        self.lfs.compilePackage(self.name, self.version, self.fmt,
            self.s, self.arc, self.is_separate_builddir,
            lambda d: buildHelper(self.s, d,
                self.preconf,
                self.configure,
                self.preinstall,
                self.postinstall))
        #except:
        #    # TODO
        #    print(format_exc())
