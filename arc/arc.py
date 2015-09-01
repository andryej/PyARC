from collections import deque

class arccachedict(object):
    ''' cache most recent gets from or sets to this dictionary

        ARC maintains two LRU lists:
            L1 = B1 + T1 - containing elements seen only once "recently"
            L2 = B2 + T2 - containing elements seen more than once "recently"

        The replacement policy deletes the LRU page in L1 if contains exactly c pages
        otherwise, it replaces the LRU page in L2
        
        Actually in cache resist only elements from T1 and T2
        
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
        self._adapt(key)
        return value

    def __setitem__(self, key, value):
        self._adapt(key)
        self._cache[key] = value

    def _adapt(self, key):
        cnt = (self._T1, self._B1, self._T2, self._B2)
        lt1, lb1, lt2, lb2 = (len(c) for c in cnt)

        """ Hit in ARC(c)
            place it at the LRU position of T2 list
        """
        if key in self._cache:
            if key in self._T1:
                self._T1.remove(key)
            if key in self._T2:
                self._T2.remove(key)
            self._T2.append(key)

        """
            Hit in DLB(2c)
            Element was seen "recently" seen only once
            place it at the MRU position of T2 list
        """
        elif key in self._B1:
            self._ratio = min(self._maxsize, self._ratio + max(1, lb2 / lb1))
            self._replace(key)
            self._B1.remove(key)
            self._T2.append(key)

        """
            Hit in DLB(2c)
            Element was seen "recently" seen only once
            place it at the MRU position of T2 list
        """
        elif key in self._B2:
            self._ratio = max(self._maxsize, self._ratio - max(1, lb1 / lb2))
            self._replace(key)
            self._B2.remove(key)
            self._T2.append(key)
        """
            No hit
            element was not seen "recently"
            place it at the MRU position of T1 list
        """
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

    def __contains__(self, key):
        return key in self._cache

    def clear(self):
        self._cache.clear()
        self._T1.clear()
        self._B1.clear()
        self._T2.clear()
        self._B2.clear()
        self._ratio = 0

    """
        According to the size of lists and a value of ratio
        delete element from cache
    """
    def _replace(self, key):
        l = len(self._T1)
        if l > 0 and (self._ratio < l or (l == self._ratio and key in self._B2)):
            x = self._T1.popleft()
            self._B1.append(x)
        else:
            x = self._T2.popleft()
            self._B2.append(x)
        del self._cache[x]
