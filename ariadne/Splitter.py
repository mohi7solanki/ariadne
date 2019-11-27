from abc import abstractmethod
import re

DEFAULT_REGEX_PATH_DELIMITER = re.compile(r'[\.-/]')
DEFAULT_STRING_PATH_DELIMITER = '.'

class BaseSplitter(object):

    def __init__(self, splitter):
        self.splitter = splitter 

    def split(self, string):
        pos = self.split_pos(string)
        return (string[:pos], string[pos+1:]) if pos else (string, None)

    @abstractmethod
    def split_pos(self, string):
        pass

class RegexSplitter(BaseSplitter):

    def __init__(self, splitter=DEFAULT_REGEX_PATH_DELIMITER):
        super().__init__(splitter)

    def split_pos(self, string):
        match = self.splitter.search(string)
        if match:
            pos = match.start()
            return pos

class StringSplitter(BaseSplitter):

    def __init__(self, splitter=DEFAULT_STRING_PATH_DELIMITER):
        super().__init__(splitter)

    def split_pos(self, string):
        pos = string.find(self.splitter)
        if pos != -1:
            return pos