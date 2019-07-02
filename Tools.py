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

from chmod_util       import chmod_a_plus_wt
from disk_util        import toBytes
from string_util      import chomp
from drop_privileges  import dropChildPrivileges
from LFSAbs           import LFSAbs
from parallel_util    import parallelize
from eintr_retry_call import _eintr_retry_call
from phash_c_download import phash_c_download_stats
from ToolsChild       import ToolsChild

from lfs_util import createRamdisk
from lfs_util import removeRamdisk
from lfs_util import makeflagFormula

""" http://www.linuxfromscratch.org/lfs/view/development """
class Tools(LFSAbs):
    def createImagePath(self):
        d = self.pathdir
        if not isdir(d): mkdir(d)
        createRamdisk(d)
    def removeImagePath(self):
        d = self.pathdir
        Tools.removeRamdisk(d)
        rmdir(d)
    def createSrcx(self):
            mkdir(self.srcx)
            createRamdisk(self.srcx)
    def removeSrcx(self):
            removeRamdisk(self.srcx)
            rmdir(self.srcx)

    def __init__(self):
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
        self.lfs_tgt = '%s-lfs-linux-gnu' % uname()[4]
    def cleanupAndBuildDistro(self):
       self.forceCleanup()
       self.buildDistro()
    def forceCleanup(self):
        print("force cleanup")
        try:    self.removeSrcx()
        except: pass
        try:    self.removeLFSUser()
        except: pass
        try:    self.removeToolsDirectory()
        except: pass
        try:    self.forceUnmountPartitions()
        except: pass
        try:    self.removeDisk()
        except: pass
    def cleanup(self):
        print("cleanup")
        self.removeSrcx()
        self.removeLFSUser()
        self.removeToolsDirectory()
        self.unmountPartitions()
        self.removeDisk()
    def cpSources(self):
        print("copy sources")
        copytree(self.sources, self.cpsrc)
    def buildDistro(self):
        print("build distro")
        """ II 2 """
        """ https://www.simplifiedpython.net/python-threading-example/ """
        def prepareHostSystem():
            print("prepare host system")
            self.createDisk()
            self.partitionDisk()
            self.createFileSystems()
            self.mountPartitions()
        diskThread   = Thread(target=prepareHostSystem)
        sourceThread = Thread(target=self.downloadSources)
        toolsThread  = Thread(target=self.createToolsDirectory)
        userThread   = Thread(target=self.createLFSUser1)
        srcxThread   = Thread(target=self.createSrcx)

        #try:
        diskThread  .start()
        sourceThread.start()
        userThread  .start()

        diskThread  .join()
        srcxThread  .start()
        toolsThread .start()
        sourceThread.join()
        # TODO start source copy thread
        toolsThread .join()
        userThread  .join()
        srcxThread  .join()

        self.createLFSUser2()
        cpThread = Thread(target=self.cpSources)
        cpThread.start()

        def child1():
            print("child process (phase 1)")                
            #self.setupEnvironment()
            #self.aboutSBUs()
            #self.constructTemporarySystem()
            c = ToolsChild(self)
            c.buildDistro()
        cpThread.join()
        dropChildPrivileges(child1, uid_name=self.user, gid_name=self.group)
        print("parent process (phase 1)")
        # TODO backup tools
        #finally: self.cleanup()
        #finally: self.forceCleanup()
            #self.removeLFSUser()
            #self.removeToolsDirectory()
            #self.unmountPartitions()
            #self.removeDisk()
        """
        try:
            self.createDisk()
            self.partitionDisk()
            self.createFileSystems()
            self.mountPartitions()
            try:
                # TODO run concurrently with previous commands
                self.downloadSources()
                self.createToolsDirectory()
                try:
                    self.createLFSUser()
                    try:
                        def child():
                            self.setupEnvironment()
                            self.constructTemporarySystem()
                            self.installSystemSoftware()
                            self.configureSystem()
                            self.makeBootable()
                        # TODO wait for previous commands to finish
                        dropChildPrivileges(child)
                    finally:
                        self.removeLFSUser()
                finally:
                    self.removeToolsDirectory()
            finally:
                self.unmountPartitions()
        finally:
            self.removeDisk()
        """

    def createDisk(self):
        print("create disk")
        self.createImagePath()

        """ https://stackoverflow.com/questions/12654772/create-empty-file-using-python """
        basedir = _eintr_retry_call(dirname, self.path)
        if not exists(basedir): _eintr_retry_call(makedirs, basedir)
        """ https://www.tutorialspoint.com/python/file_truncate.htm """
        with open(self.path, 'wb') as f: _eintr_retry_call(lambda F: F.truncate(self.sz), f)
    def removeDisk(self):
        print("remove disk")
        _eintr_retry_call(remove, self.path)
        self.removeImagePath()

    """ II 2.4 """
    def partitionDisk(self):
        print("partition disk")
        #check_call(['sgdisk', '-go', path])
        #check_call(['sgdisk', '-n1:%s:%s' % (toBytes("1 GB"), toBytes("10 GB")), path])
        pass

    """ II 2.5 """
    def createFileSystems(self):
        print("create file systems")
        # TODO multithread
        #check_call(['mkfs.ext2', path]) # /boot
        check_call(['mkfs', '-t', self.fstype, self.path], stdin=DEVNULL, stdout=DEVNULL) # /
        #check_call(['mkfs.ext2', path]) # /usr
        #check_call(['mkfs.ext2', path]) # /var
        #check_call(['mkfs.ext2', path]) # /tmp
        #check_call(['mkfs.ext2', path]) # /srv
        #check_call(['mkfs.ext2', path]) # /opt
        #check_call(['mkfs.ext2', path]) # /home
        #check_call(['mkfs.ext2', path]) # swap

    """ II 2.7 """
    """ https://stackoverflow.com/questions/20406422/mounting-a-partition-inside-a-dd-image-with-python """
    def mountPartitions(self):
        print("mount partitions")
        _eintr_retry_call(mkdir, self.lfs)
        check_call(['losetup', self.lo, self.path], stdin=DEVNULL, stdout=DEVNULL)
        check_call(['mount', '-t', self.fstype, self.lo, self.lfs], stdin=DEVNULL, stdout=DEVNULL)
    def unmountPartitions(self):
        print("unmount partitions")
        check_call(['umount', self.lfs], stdin=DEVNULL, stdout=DEVNULL)
        check_call(['losetup', '-d', self.lo], stdin=DEVNULL, stdout=DEVNULL)
        _eintr_retry_call(rmdir, self.lfs)
    def forceUnmountPartitions(self):
        print("force unmount partitions")
        try:    check_call(['umount', self.lfs], stdin=DEVNULL, stdout=DEVNULL)
        except: pass
        try:    check_call(['losetup', '-d', self.lo], stdin=DEVNULL, stdout=DEVNULL)
        except: pass
        try:    _eintr_retry_call(rmdir, self.lfs)
        except: pass

    """ II 4.2 """
    
    def createToolsDirectory(self):
        print("create tools directory")
        #mkdir (self.tools)
        #symlink(self.tools, self.toolsym)
        #t1 = Thread(target=mkdir,   args=[self.tools])
        #t2 = Thread(target=symlink, args=[self.tools, self.toolsym])
        #t1.start()
        #t2.start()
        #t1.join()
        #t2.join()
        def mktools():
            mkdir(self.tools)
            createRamdisk(self.tools)

        #parallelize([
        #    (_eintr_retry_call, [mktools]),
        #    (_eintr_retry_call, [symlink, self.tools, self.toolsym])
        #])
        mktools()
        symlink(self.tools, self.toolsym)
    def removeToolsDirectory(self):
        print("remove tools directory")
        #rmtree(self.tools)
        #remove(self.toolsym)
        #t1 = Thread(target=rmtree, args=[self.tools])
        #t2 = Thread(target=remove, args=[self.toolsym])
        #t1.start()
        #t2.start()
        #t1.join()
        #t2.join()
        def rmtools():
            removeRamdisk(self.tools)
            rmdir(self.tools)
        parallelize([
            #(_eintr_retry_call, [rmtree, self.tools]),
            (_eintr_retry_call, [rmtools]),
            (_eintr_retry_call, [remove, self.toolsym])
        ])

    """ II 4.3 """
    """ https://pagure.io/libuser/blob/master/f/python/test-script """
    def createLFSUser(self):
        print("create LFS user")
        ##admin = libuser.admin()
        ##jimbo = admin.initUser(self.user)
        ###jimbo[libuser.HOMEDIRECTORY] = '/var/jimbo-home'
        ##admin.addUser(jimbo)
        ##return admin, jimbo
        #check_call(['groupadd', self.group])
        #check_call(['useradd', '-s', join(sep, "bin", "bash"), '-g', self.group, '-m', '-k', join(sep, "dev", "null"), self.user])
        #chown(self.tools,   self.group, self.user)
        #chown(self.sources, self.group, self.user)
        ##self.groups, self.old_umask = drop_eprivileges(uid_name=self.user, gid_name=self.group)
        self.createLFSUser1()
        self.createLFSUser2()
    def createLFSUser1(self):
        print("create LFS user (stage 1)")
        check_call(['groupadd', self.group], stdin=DEVNULL, stdout=DEVNULL)
        check_call(['useradd', '-s', join(sep, "bin", "bash"), '-g', self.group, '-m', '-k', join(sep, "dev", "null"), self.user], stdin=DEVNULL, stdout=DEVNULL)
    def createLFSUser2(self):
        print("create LFS user (stage 2)")
        #chown(self.tools,   self.group, self.user)
        #chown(self.sources, self.group, self.user)
        #t1 = Thread(target=chown, args=[self.tools,   self.group, self.user])
        #t2 = Thread(target=chown, args=[self.sources, self.group, self.user])
        #t1.start()
        #t2.start()
        #t1.join()
        #t2.join()
        parallelize([
            (_eintr_retry_call, [chown, self.tools,   self.group, self.user]),
            (_eintr_retry_call, [chown, self.sources, self.group, self.user]),
            (_eintr_retry_call, [chown, self.srcx,    self.group, self.user])
        ])

    def removeLFSUser(self):
        print("remove LFS user")
        ##restore_eprivileges(self.groups, self.old_umask)
        ##admin.deleteUser(jimbo)
        ##admin.removeHome(jimbo)
        ##admin.removeMail(jimbo)
        home = _eintr_retry_call(getpwnam, self.user).pw_dir
        check_call(['userdel', self.user], stdin=DEVNULL, stdout=DEVNULL)
        ##check_call(['groupdel', self.user])
        ## TODO
        ##home = expanduser("~%s" % self.user)
        ##home = "/home/%s" % self.user
        _eintr_retry_call(rmtree, home)
        #home = getpwnam(self.user).pw_dir
        #t1 = Thread(target=check_call, args=[['userdel', self.user]])
        #t2 = Thread(target=rmtree,     args=[home])
        #t1.start()
        #t2.start()
        #t1.join()
        #t2.join()
        #parallelize([
        #    (check_call, ['userdel', self.user]),
        #    (rmtree,     [home])
        #])
        
    """ II 3.1 """
    """ https://stackabuse.com/download-files-with-python/ """
    def downloadSources(self):
        print("download sources")
        if not _eintr_retry_call(isdir, self.sources): _eintr_retry_call(mkdir, self.sources)
        _eintr_retry_call(chmod_a_plus_wt, self.sources)
        # TODO
        #wget --input-file=wget-list --continue --directory-prefix=$LFS/sources
        wgetList = "%s/wget-list" % self.lfs_dns
        md5sums  = "%s/md5sums"   % self.lfs_dns
        missing_urls, missing_hashes, correct_hashes, failed_hashes = phash_c_download_stats(wgetList, md5sums, self.sources)
        print("correct hashes: %s" % correct_hashes)
        """
        # TODO select a reasonable number of threads for the total download rate vs max download bandwidth
        " "" https://stackoverflow.com/questions/6194499/pushd-through-os-system "" "
        previous_dir = _eintr_retry_call(getcwd)
        _eintr_retry_call(chdir, self.sources)
        try:
            #downloadIfNewer('http://www.linuxfromscratch.org/lfs/view/development/wget-list')
            #p = Pool()
            #with open('wget-list') as w:
                #urls = w.readlines()
                #urls = LFS.chomp(w.readlines())
            #    urls = map(chomp, w.readlines())
            #p.map(LFS.downloadURL, urls)
            #p.close()
            #p.join()
            #pdownloadList('http://www.linuxfromscratch.org/lfs/view/development/wget-list')

            #map(LFS.downloadURL, urls)
            #for url in urls: downloadURL(url)

            #downloadIfNewer('http://www.linuxfromscratch.org/lfs/view/development/md5sums')

            #t1 = Thread(target=pdownloadList,   args=['http://www.linuxfromscratch.org/lfs/view/development/wget-list'])
            #t2 = Thread(target=downloadIfNewer, args=['http://www.linuxfromscratch.org/lfs/view/development/md5sums'])
            #t1.start()
            #t2.start()
            #t1.join()
            #t2.join()

            parallelize([
                (_eintr_retry_call, [pdownloadList,   'http://www.linuxfromscratch.org/lfs/view/development/wget-list', self.sources]),
                (_eintr_retry_call, [downloadIfNewer, 'http://www.linuxfromscratch.org/lfs/view/development/md5sums', self.sources])
            ])

            #with open('md5sums') as m:
            #    md5s = m.readlines()
            #for md5 in md5s:
            #    m = md5()
            #    m.update()
            #    if m.digest() is not md5: raise Error()

            #pushd $LFS/sources
            #md5sum -c md5sums
            #popd
            
            #cnt = md5_c_open(join(self.sources, 'md5sums'), self.sources)
            cnt = sum(pmd5_c_open(join(self.sources, 'md5sums'), self.sources))
            print("correct hashes: %s" % cnt)
            #check_call(['md5sum', '-c', 'md5sums'])
        finally: _eintr_retry_call(chdir, previous_dir)
        """

    
def main():
    if getuid() != 0: raise Exception()

    # TODO need distcc + ccache
    lfs  = Tools()
    try:     lfs.cleanupAndBuildDistro()
    finally: lfs.forceCleanup()
    # TODO reboot into qemu vm & finish compiling
    #blfs = BLFS(lfs)
    #blfs.buildDistro()
    # TODO install to zeroed disk
    # TODO compress and ramboot
    # TODO reboot into qemu vm & run integration test
    # TODO install
    # TODO put wm (and other progs?) in docker
if __name__ == "__main__": main()
