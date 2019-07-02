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



""" https://www.jamescoyle.net/how-to/943-create-a-ram-disk-in-linux """
def createRamdisk(path, sz=None):
    if sz is None: szopt = []
    else:          szopt = ['-o', 'size=%s' % sz]
    check_call(['mount', '-t', 'tmpfs'] + szopt + ['tmpfs', path], stdin=DEVNULL, stdout=DEVNULL)

def removeRamdisk(path): check_call(['umount', path], stdin=DEVNULL, stdout=DEVNULL)

def makeflagFormula(nproc): return nproc * 2 + 1


