from grp        import getgrnam
from subprocess import check_call

""" https://stackoverflow.com/questions/2540460/tell-if-a-given-login-exists-in-linux-using-python """
def groupexists(group):
    try:
        getgrnam(group)
        return True
    except KeyError: return False

def groupadd(group): check_call(['groupadd', group])

def groupdel(group): check_call(['groupdel', group])

def main():
    group = "groupadd"
    if groupexists(group): raise Error()
    groupadd(group)
    assert groupexists(group)
    groupdel(group)
if __name__ == "__main__": main()
