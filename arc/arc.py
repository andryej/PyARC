from collections import deque

class arccachedict(object):
    '''cache most recent gets from or sets to this dictionary'''
    def __init__(self, maxsize):
        self._cache = {}
        self._T1 = deque()
        self._B1 = deque()
        self._T2 = deque()
        self._B2 = deque()
        self._maxsize = maxsize
        self._ratio = 0

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __contains__(self, key):
        return self._cache.contains(key)

    def clear(self):
        self._cache.clear()
        self._T1.clear()
        self._B1.clear()
        self._T2.clear()
        self._B2.clear()
        self._ratio = 0

    def _adapt(x):
        pass

    def _replace():
        pass

def arccachefunc(func):
    pass
