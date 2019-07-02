from LFSAbs import LFSAbs
from LFS    import LFS

""" http://www.linuxfromscratch.org/blfs/view/svn """
class BLFS(LFSAbs):
    def __init__(self, lfs):
        self.lfs = lfs
    def buildDistro(self):
        pass

def main():
    # TODO need distcc + ccache
    tools = Tools()
    lfs   = LFS(tools)
    blfs  = BLFS(lfs)
    try:
        tools.cleanupAndBuildDistro()
        lfs  .buildDistro()
        # TODO reboot into qemu vm & finish compiling
        blfs .buildDistro()
    finally:
        blfs .forceCleanup()
        lfs  .forceCleanup()
        tools.forceCleanup()

    # TODO install to zeroed disk
    # TODO compress and ramboot
    # TODO reboot into qemu vm & run integration test
    # TODO install
    # TODO put wm (and other progs?) in docker
if __name__ == "__main__": main()
