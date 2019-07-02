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
from pwd             import getpwnam
from shutil          import chown
from shutil          import copyfile
from shutil          import copytree
from shutil          import rmtree
from subprocess      import check_call

from chmod_util       import chmod_a_plus_wt
from disk_util        import toBytes
from string_util      import chomp
from drop_privileges  import dropChildPrivileges
from LFSAbs           import LFSAbs
from parallel_util    import parallelize
from eintr_retry_call import _eintr_retry_call
from phash_c_download import phash_c_download_stats

""" http://www.linuxfromscratch.org/lfs/view/development """
class LFS(LFSAbs):
    def __init__(self, tools):
        self.tools = tools

        # TODO store on ram disk
        """ https://stackoverflow.com/questions/17429044/constructing-absolute-path-with-os-path-join#28080468 """
        self.pathdir = join(sep, 'mnt', 'imgs')
        self.path    = join(self.pathdir, 'lfs.img')
        #self.path    = join(sep, "lfs.img")
        self.fstype  = 'ext2'
        # TODO use temp dir
        self.lfs     = join(sep, "mnt", "lfs")
        self.sz      = toBytes(['20 GB'])[0]
        # TODO
        self.lo      = join(sep, "dev", "loop1")
        # TODO use temp dir
        # TODO use ram disk
        self.tools   = join(self.lfs, "tools")
        self.toolsym = join(sep,      "tools")
        self.sources = join(sep,      "sources")
        self.cpsrc   = join(self.lfs, "sources")
        self.srcx    = join(self.lfs, "srcx")
        self.lfs_dns = 'http://www.linuxfromscratch.org/lfs/view/development'
        self.group   = 'lfs'
        self.user    = 'lfs'
    def cleanupAndBuildDistro(self):
       self.forceCleanup()
       self.buildDistro()
    def forceCleanup(self):
        print("force cleanup")
    def cleanup(self):
        print("cleanup")
    def buildDistro(self):
        print("build distro")
        """ II 2 """
        def child2():
            print("child process (phase 2)")
            self.installSystemSoftware()
            self.configureSystem()
            self.makeBootable()
        dropChildPrivileges(child2, uid_name=self.user, gid_name=self.group)
        print("parent process (phase 2)")


    """ II 5 """
    def constructTemporarySystem(self):
        print("construct temporary system")
        # TODO
        check_call(['ls', self.sources])
        pass
    """ III 6 """
    def installSystemSoftware(self):
        print("install system software")
        # TODO copy sources from host to dest before entering chroot
        # copy can be done concurrently with constructTemporarySystem()
        pass
    """ III 7 """
    def configureSystem(self):
        print("configure system")
        # TODO
        pass
    """ III 8 """
    def makeBootable(self):
        print("make bootable")
        # TODO
        pass

    """ II 5.3 """
    def compilePackage(pkg, build):
        # TODO move sources
        old_dir = getcwd()
        #chdir(self.sources)
        try:
            # TODO extract to temp dir
            # TODO use ram disk
            # tar xf pkg
            """ https://stackoverflow.com/questions/31163668/how-do-i-extract-a-tar-file-using-python-2-4#31163747 """
            with tarfile.open(pkg, 'r') as tar: tar.extractall(pkgdir)
            #pkgdir = join(sep, self.sources, pkg?)
            #chdir(pkgdir)
            #build()
        finally:
            #chdir(self.sources)
            t = Thread(target=rmtree, args=[pkgdir])
            t.start()
            chdir(old_dir)
            return t

def main():
    if getuid() != 0: raise Exception()

    tools = Tools()
    lfs   = LFS(tools)
    try:
        tools.cleanupAndBuildDistro()

    # TODO need distcc + ccache

    #lfs.cleanupAndBuildDistro()
        lfs.buildDistro()
    finally:
        lfs.forceCleanup()
        tools.forceCleanup()
    # TODO reboot into qemu vm & finish compiling
    #blfs = BLFS(lfs)
    #blfs.buildDistro()
    # TODO install to zeroed disk
    # TODO compress and ramboot
    # TODO reboot into qemu vm & run integration test
    # TODO install
    # TODO put wm (and other progs?) in docker
if __name__ == "__main__": main()
