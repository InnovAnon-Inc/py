from grp        import getgrnam
from os         import _exit
from os         import fork
from os         import getgroups
from os         import getgid
from os         import getuid
from os         import setegid
from os         import seteuid
from os         import setgid
from os         import setgroups
from os         import setuid
from os         import umask
from os         import waitpid
from pwd        import getpwnam

from eintr_retry_call import _eintr_retry_call

# TODO restartability

""" https://stackoverflow.com/questions/2699907/dropping-root-permissions-in-python """
def drop_privileges(uid_name='nobody', gid_name='nogroup'):
    if getuid() != 0:
        # We're not root so, like, whatever dude
        return

    # Get the uid/gid from the name
    running_uid = getpwnam(uid_name).pw_uid
    running_gid = getgrnam(gid_name).gr_gid

    # Remove group privileges
    setgroups([])

    # Try setting the new uid/gid
    setgid(running_gid)
    setuid(running_uid)

    # Ensure a very conservative umask
    old_umask = umask(0o077)

""" https://code-maven.com/parallel-processing-using-fork-in-python """
def dropChildPrivileges(child, uid_name='nobody', gid_name='nogroup'):
    #try:
    pid = fork()
    #except OSError:

    if pid is 0:
        try:
            drop_privileges(uid_name=uid_name, gid_name=gid_name)
            child()
        finally: _exit(0)
    #waitpid(pid, 0)
    _eintr_retry_call(waitpid, pid, 0)

""" https://stackoverflow.com/questions/25928190/python-run-command-as-normal-user-in-a-root-script """
def drop_eprivileges(uid_name='nobody', gid_name='nogroup'):
    if getuid() != 0:
        # We're not root so, like, whatever dude
        return

    # Get the uid/gid from the name
    running_uid = getpwnam(uid_name).pw_uid
    running_gid = getgrnam(gid_name).gr_gid

    groups = getgroups()

    # Remove group privileges
    setgroups([])

    # Try setting the new uid/gid
    setegid(running_gid)
    seteuid(running_uid)

    # Ensure a very conservative umask
    old_umask = umask(0o077)

    return groups, old_umask
def restore_eprivileges(groups, old_umask):
    umask(old_umask)
    seteuid(getuid())
    setegid(getgid())
    setgroups(groups)

def main():
    groups, old_umask = drop_eprivileges()
    restore_eprivileges(groups, old_umask)
    def child(): print("in child")
    dropChildPrivileges(child)
    drop_privileges()
if __name__ == "__main__": main()
