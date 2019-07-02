from functools       import reduce
from itertools       import product
from multiprocessing import Pool
from os              import chmod
from os              import stat as osstat
from os              import umask
from re              import compile
from re              import findall
from stat            import S_ISUID

import stat

from static_vars     import static_vars
from parallel_util   import parallelize

""" https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python """
def get_umask(): return umask(umask(0))

def chmod_a_plus_wt(path):
    """
    chmod(
        path,
        stat(path).st_mode |
        (
            (
                S_IWUSR |
                S_IWGRP |
                S_IWOTH |
                S_ISUID
            )
            & ~LFS.get_umask()
        )
    )
    """
    parseChmod(path, "a+wt")

@static_vars(scopeRe = compile("[ugoa]*"),
             opRe    = compile("[=+-]"  ),
             permRe  = compile("[rwxt]*"))
def parseChmod(path, flags):
    """ https://stackoverflow.com/questions/10663093/use-python-format-string-in-reverse-for-parsing """
    scopeMat = findall(parseChmod.scopeRe, flags, flags=0)
    opMat    = findall(parseChmod.opRe,    flags, flags=0)
    permMat  = findall(parseChmod.permRe,  flags, flags=0)

    scope = ''.join(scopeMat)
    op    = ''.join(opMat)
    perm  = ''.join(permMat)

    scope = 'u'   if not scope        else scope
    scope = 'ugo' if     scope == 'a' else scope

    if 't' in perm:
        issuid = True
        perm   = perm.replace('t', "")
    else: issuid = False

    ezChmod(path, scope, op, perm, issuid)

def ezChmodHelper(a): return getattr(stat, "S_I%s%s" % a)

""" https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python """
@static_vars(scopes = { 'u' : 'USR', 'g' : 'GRP', 'o' : 'OTH' },
             perms  = { 'r' : 'R',   'w' : 'W',   'x' : 'X'   },
             ops    = { '=' : lambda p, path : 0                    |  p,
                        '+' : lambda p, path : osstat(path).st_mode |  p,
                        '-' : lambda p, path : osstat(path).st_mode & ~p })
def ezChmod(path, scope, op, perm, issuid):
    myScopes = map(lambda s: ezChmod.scopes[s], scope)
    myPerms  = map(lambda p: ezChmod.perms[p],  perm)
    pool = Pool()
    cons     = pool.map(ezChmodHelper, product(myPerms, myScopes))
    pool.close()
    pool.join()
    #cons     = map   (lambda a: getattr(stat, "S_I%s%s" % a), product(myPerms, myScopes))
    P        = reduce(lambda a, b: a | b, cons, S_ISUID if issuid else 0)
    f        = ezChmod.ops[op]
    fp       = f(P, path)
    chmod(path, fp)

def main():
    #LFSChmodUtil.ezChmod('test.txt', 'ugo', '+', 'w', True)
    parseChmod('test.txt', 'a+wt')
    #LFSChmodUtil.chmod_a_plus_wt('test.txt')
if __name__ == "__main__": main()
