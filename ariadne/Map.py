from abc import ABCMeta, abstractmethod
from collections.abc import Mapping, MutableMapping

import re

try:
    import pyyaml
except ImportError:
    pass

def __string_path_splitter(delimiter, path):
    pos = path.find(delimiter)
    if pos != -1:
        return pos

def __regex_path_splitter(delimiter, path):
    match = delimiter.search(path)
    if match:
        pos = match.start()
        return pos

DEFAULT_PATH_DELIMITER = re.compile(r'[\.-/]')

class Map(MutableMapping, metaclass=ABCMeta):

    def __init__(self, map_obj=dict(), delimiter=DEFAULT_PATH_DELIMITER):
        self._map = map_obj
        self.splitter = self._init_path_splitter(delimiter)

    # overloaded operators

    def __getattr__(self, path):
        return self.__getitem__(path)

    def __getitem__(self, path):
        l, r = self._split_and_splice(path)
        return self._map[l][r] if r else self._map[l]

    def __setitem__(self, path, value):
        l, r = self._split_and_splice(path)

        if r:
            temp = Map(delimiter=self.delimiter)
            temp[r] = value
            value = temp[r]

        self._map[l] = value

    def __delattr__(self, path):
        self.__delitem__(path)

    def __delitem__(self, path):
        l, r = self._split_and_splice(path)
        self._map[l].__delitem__(r) if r else self._map.__delitem__(l)

    def __iter__(self):
        return self._map.__iter__()

    def __len__(self):
        return self.map.__len__()

    # private methods

    def _init_path_splitter(self, delimiter):
        if isinstance(delimiter, str):
            return lambda path: __string_path_splitter(delimiter, path)
        if isinstance(delimiter, re.Pattern):
            return lambda path: __regex_path_splitter(delimiter, path)
        raise TypeError('The delimiter argument must be a string or a regex pattern object')

    def _split_and_splice(self, path):
        l, r = self._split_path(path)
        self._splice(l)
        return l, r

    def _splice(self, l):
        if l in self._map.keys() and isinstance(self._map[l], Mapping):
            self._map[l] = Map(self._map[l], delimiter=self.delimiter)

    def _split_path(self, path):
        pos = self._splitter(path)
        if pos:
            return path[:pos], path[pos+1:]
        return path, None