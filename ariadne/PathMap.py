from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping

import re

class PathMap(MutableMapping, metaclass=ABCMeta):

    PATH_DELIMITERS = r'[\.-/]'

    def __init__(self, delimiters=PATH_DELIMITERS):
        self._map = {}
        self.delimiters = re.compile(delimiters)

    def _split_path(self, path):
        match = self.delimiters.search(path)
        if match:
            p = match.start()
            return path[:p], path[p+1:]
        return path, None

    def __getattr__(self, path):
        return self.__getitem__(path)

    def __getitem__(self, path):
        l, r = self._split_path(path)
        return self._map[l][r] if r else self._map[l]

    def __setitem__(self, path, value):
        l, r = self._split_path(path)
        
        # if already some kinf of map, then splice
        if l in self._map.keys() and isinstance(self._map[l], dict):
            replacement = PathMap()
            replacement._map = self._map[l]
            self._map[l] = replacement

        if r:
            node = PathMap(delimiters=self.delimiters)
            node[r] = value
        else:
            node = value
        
        self._map[l] = node

    def __delitem__(self, path):
        l, r = self._split_path(path)
        self._map[l].__delitem__(r) if r else self._map.__delitem__(l)

    def __iter__(self):
        return self._map.__iter__()

    def __len__(self):
        return self.map.__len__()