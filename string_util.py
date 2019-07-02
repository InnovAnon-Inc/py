def chomp(s): return s[:-1] if s[-1] is '\n' else s

def main():
    s = """abc
"""
    t = """abc"""
    assert chomp(s) == chomp(t)
if __name__ == "__main__": main()
