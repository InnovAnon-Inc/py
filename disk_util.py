""" https://stackoverflow.com/questions/39284008/how-to-convert-mb-to-gb-with-precision-in-python """
def toBytes(sizes):
    defs={'KB':1024, 'MB':1024**2, 'GB':1024**3, 'TB':1024**4} 
    bytes=[float(lh)*defs[rh] for lh, rh in [e.split() for e in sizes]]
    return bytes

def main():
    s = ["%s %s" % (k, p)
            for p in ['KB', 'MB', 'GB', 'TB']
                for k in range(1, 10)]
    for k, p in zip(s, toBytes(s)): print("%s = %s" % (k, p))
if __name__ == "__main__": main()
