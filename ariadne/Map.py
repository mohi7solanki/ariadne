from abc import ABCMeta
from collections import defaultdict
from collections.abc import Mapping, MutableMapping
from .Splitter import BaseSplitter, RegexSplitter

try:
    import pyyaml
except ImportError:
    pass

SPECIAL_KEYS = ['_internal_map', '_splitter']

class Map(MutableMapping, metaclass=ABCMeta):

    def __init__(self, source=None, splitter=RegexSplitter(), createdonaccess=False):
        if not callable(splitter):
            raise TypeError('The splitter must be callable')
        self._splitter = splitter
        self._internal_map = source or dict()
        self._createdonaccess = createdonaccess

    def __getattr__(self, path):
        try:
            return self.__getitem__(path)
        except KeyError:
            self._internal_map[path] = Map(splitter=self._splitter, createdonaccess=True)
            return self.__getattr__(path)

    def __getitem__(self, path):
        l, r = self._split_and_splice(path)
        return self._internal_map[l][r] if r else self._internal_map[l]

    def __setattr__(self, path, value):
        if path in SPECIAL_KEYS:
            super().__setattr__(path, value)
        else:
            self.__setitem__(path, value)

    def __setitem__(self, path, value):
        l, r = self._split_and_splice(path)
        if r:
            temp = Map(splitter=self._splitter)
            temp[r] = value
            value = temp
        self._internal_map[l] = value

    def __delattr__(self, path):
        self.__delitem__(path)

    def __delitem__(self, path):
        l, r = self._split_and_splice(path)
        self._internal_map[l].__delitem__(r) if r else self._internal_map.__delitem__(l)

    def __iter__(self):
        return self._internal_map.__iter__()

    def __len__(self):
        return self.map.__len__()

    def _split_and_splice(self, path):
        l, r = self._splitter(path)
        self._splice(l)
        return l, r

    def _splice(self, l):
        if l in self._internal_map.keys():
            if isinstance(self._internal_map[l], Mapping) and not isinstance(self._internal_map[l], type(self)):
                self._internal_map[l] = Map(self._internal_map[l], splitter=self._splitter)