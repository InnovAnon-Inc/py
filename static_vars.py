""" https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function#279586 """
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        #map(lambda k: setattr(func, k, kwargs[k]), kwargs)
        return func
    return decorate
