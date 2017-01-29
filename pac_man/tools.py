import time


def timeit(f):

    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print('func:{funcname} took: {time:.4f} sec'.format(
              funcname=f.__name__, time=te-ts))
        return result
    return timed
