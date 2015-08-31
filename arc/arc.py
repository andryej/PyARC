from collections import deque

class arccachedict(object):
    ''' cache most recent gets from or sets to this dictionary

        ARC maintains two LRU lists:
            L1 = B1 + T1 - containing elements seen only once "recently"
            L2 = B2 + T2 - containing elements seen more than once "recently"

        The replacement policy deletes the LRU page in L1 if contains exactly c pages
        otherwise, it replaces the LRU page in L2
    '''

    def __init__(self, maxsize):
        self._cache = {}
        self._T1 = deque()
        self._B1 = deque()
        self._T2 = deque()
        self._B2 = deque()
        self._maxsize = maxsize
        self._ratio = 0

    def __getitem__(self, key):
        value = self._cache[key]
        if key in self._cache:
            self.__setitem__(key, value)
        return value

    def __setitem__(self, key, value):
        cnt = (self._T1, self._B1, self._T2, self._B2)
        lt1, lb1, lt2, lb2 = (len(c) for c in cnt)

        if key in self._cache:
            (t.remove(key) for t in (self._T1, self._T2) if key in t)
            self._T2.append(key)

        elif key in self._B1:
            p = min(self._maxsize, p + max(1, lb2 / lb1))
            self._replace(key)
            self._B1.remove(key)
            self._T2.append(key)

        elif key in self._B2:
            p = max(self._maxsize, p - max(1, lb1 / lb2))
            self._replace(key)
            self._B2.remove(key)
            self._T2.append(key)

        else:
            if lt1 + lb1 == self._maxsize:
                if lt1 < self._maxsize:
                    self._B1.popleft()
                    self._replace(key)
                else:
                    del self._cache[self._T1.popleft()]
            else:
                sm = lt1 + lt2 + lb1 + lb2
                if sm >= self._maxsize:
                    if sm == 2*self._maxsize:
                        self._B2.popleft()
                    self._replace(key)

        self._T1.append(key)
        self._cache[key] = value

    def __contains__(self, key):
        return key in self._cache

    def clear(self):
        self._cache.clear()
        self._T1.clear()
        self._B1.clear()
        self._T2.clear()
        self._B2.clear()
        self._ratio = 0

    def _replace(self, key):
        l = len(self._T1)
        if l > 0 and (x in self._B2 or l > p):
            x = self.T1.popleft()
            self._B1.append(x)
        else:
            x = self.T2.popleft()
            self._B2.append(x)
        del self._cache[x]
