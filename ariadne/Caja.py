from abc import ABCMeta
from collections import defaultdict
from collections.abc import Mapping, MutableMapping, Sequence, MutableSequence
from .Splitter import BaseSplitter, RegexSplitter

try:
    import pyyaml
except ImportError:
    pass

SPECIAL_KEYS = ['_internal_structure_', '_splitter_', '_createdonaccess_']

class Caja(MutableMapping, metaclass=ABCMeta):

    __InternalStructureTypes__ = ( dict, list, type(None) )

    def __init__(self, source=None, splitter=RegexSplitter(), createdonaccess=False):
        if not callable(splitter):
            raise TypeError('The splitter must be callable')
        
        self._splitter_ = splitter
        self._createdonaccess_ = createdonaccess
        self._internal_structure_ = self.__process_source__(source)


    def raw(self):
        
        # prepare object and list of keys/indices
        root = self._internal_structure_
        if isinstance(root, dict):
            ks = root.keys()
            obj  = {}
        elif isinstance(root, list):
            ks = range(len(root))
            obj  = []

        # rebuild raw structure
        for k in ks:
            if isinstance(root[k], type(self)):
                if not root[k]._createdonaccess_:
                    obj[k] = root[k].raw()
            else:
                obj[k] = root[k]

        return obj


    def __process_source__(self, source):
        if not isinstance(source, self.__InternalStructureTypes__):
            raise TypeError("source argument must be either, None, dict, or list")
        
        return source if source else dict()


    def __getattr__(self, path):
        # if created on access and not 
        try:
            return self.__getitem__(path)
        except KeyError:
            self._internal_structure_[path] = Caja(splitter=self._splitter_, createdonaccess=True)
            return self.__getattr__(path)


    def __getitem__(self, path):
        left, right = self.__split_and_splice__(path)

        if isinstance(self._internal_structure_, Sequence):
            left = int(left)

        if right:
            return self._internal_structure_[left][right]
        else:
            return self._internal_structure_[left]


    def __setattr__(self, path, value):
        if path in SPECIAL_KEYS:
            super().__setattr__(path, value)
        else:
            self.__setitem__(path, value)


    def __setitem__(self, path, value):
        left, right = self.__split_and_splice__(path)
        
        if right:
            temp = Caja(splitter=self._splitter_)
            temp[right] = value
            value = temp

        self._createdonaccess_ = False
        self._internal_structure_[left] = value


    def __delattr__(self, path):
        self.__delitem__(path)


    def __delitem__(self, path):
        left, right = self.__split_and_splice__(path)
        if right:
            self._internal_structure_[left].__delitem__(right)
        else:
            self._internal_structure_.__delitem__(left)


    def __iter__(self):
        return self._internal_structure_.__iter__()


    def __len__(self):
        return self._internal_structure_.__len__()


    def __split_and_splice__(self, path):
        left, right = self._splitter_(path)
        self.__splice__(left)
        return left, right


    def __splice__(self, key):
        root = self._internal_structure_
        if isinstance(root, list):
            k, i = int(key), range(0, len(root))
        elif isinstance(root, Mapping):
            k, i = key, root.keys()
        else:
            return

        # if under the key there is a source type, then splice it to guarantee recursion
        if k in i and isinstance(root[k], self.__InternalStructureTypes__) and not isinstance(root[k], type(self)):
            root[k] = Caja(root[k], splitter=self._splitter_)


    def __eq__(self, other):
        return (type(self) == type(other) and self._internal_structure_ == other._internal_structure_) or (self._internal_structure_ == other)
    

    def __ne__(self, other):
        return not self.__eq__(other)


    def __repr__(self):
        return self._internal_structure_.__repr__()


    def __str__(self):
        return self._internal_structure_.__str__()


    def __format__(self, format_spec):
        return self._internal_structure_.__format__(format_spec)

    
    def __bool__(self):
        return not self._createdonaccess_ and bool(self._internal_structure_)