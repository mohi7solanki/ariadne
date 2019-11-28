from abc import ABCMeta
from collections import defaultdict
from collections.abc import Mapping, MutableMapping, Sequence, MutableSequence
from .Splitter import BaseSplitter, RegexSplitter

try:
    import pyyaml
except ImportError:
    pass

SPECIAL_KEYS = ['__internal_structure__', '__splitter__', '__createdonaccess__']

class Caja(MutableMapping, metaclass=ABCMeta):

    InternalStructureTypes = ( Mapping, Sequence, type(None) )

    def __init__(self, source=None, splitter=RegexSplitter(), createdonaccess=False):
        if not callable(splitter):
            raise TypeError('The splitter must be callable')
        
        self.__splitter__ = splitter
        self.__createdonaccess__ = createdonaccess
        self.__internal_structure__ = self.__process_source__(source)


    def to_dict(self):
        pass


    def __process_source__(self, source):
        if not isinstance(source, self.InternalStructureTypes):
            raise TypeError("source argument must be either, None, Mapping, or Sequence type")
        
        return source if source else dict()


    def __getattr__(self, path):
        try:
            return self.__getitem__(path)
        except KeyError:
            self.__internal_structure__[path] = Caja(splitter=self.__splitter__, createdonaccess=True)
            return self.__getattr__(path)


    def __getitem__(self, path):
        left, right = self.__split_and_splice__(path)
        if right:
            return self.__internal_structure__[left][right]
        else:
            return self.__internal_structure__[left]


    def __setattr__(self, path, value):
        if path in SPECIAL_KEYS:
            super().__setattr__(path, value)
        else:
            self.__setitem__(path, value)


    def __setitem__(self, path, value):
        left, right = self.__split_and_splice__(path)
        
        if right:
            temp = Caja(splitter=self.__splitter__)
            temp[right] = value
            value = temp

        self.__createdonaccess__ = False
        self.__internal_structure__[left] = value


    def __delattr__(self, path):
        self.__delitem__(path)


    def __delitem__(self, path):
        left, right = self.__split_and_splice__(path)
        if right:
            self.__internal_structure__[left].__delitem__(right)
        else:
            self.__internal_structure__.__delitem__(left)


    def __iter__(self):
        return self.__internal_structure__.__iter__()


    def __len__(self):
        return self.__internal_structure__.__len__()


    def __split_and_splice__(self, path):
        left, right = self.__splitter__(path)
        self.__splice__(left)
        return left, right


    def __splice__(self, l):
        if l in self.__internal_structure__.keys():
            if isinstance(self.__internal_structure__[l], Mapping) and not isinstance(self.__internal_structure__[l], type(self)):
                self.__internal_structure__[l] = Caja(self.__internal_structure__[l], splitter=self.__splitter__)