from random     import choice
from string     import ascii_lowercase

from groupadd import groupadd
from groupadd import groupdel
from groupadd import groupexists

""" https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits#2257449 """
def id_generator(size=6, chars=ascii_lowercase):
    #return ''.join(choice(chars) for _ in range(size))
    return ''.join(map(lambda _: choice(chars), range(size)))

def groupradd():
    while True:
        group = id_generator()
        if not groupexists(group): break
    #while groupexists(group = id_generator()): pass
    groupadd(group)
    return group

def main():
    group = groupradd()
    assert groupexists(group)
    groupdel(group)
    assert not groupexists(group)
if __name__ == "__main__": main()
