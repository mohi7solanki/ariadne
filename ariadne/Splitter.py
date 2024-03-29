from abc import abstractmethod
import re

DEFAULT_REGEX_PATH_DELIMITER = re.compile(r'[\.-/]')
DEFAULT_STRING_PATH_DELIMITER = '.'

class BaseSplitter():

    def __init__(self, splitter):
        self.splitter = splitter 

    def split(self, string):
        if isinstance(string, str):
            range_pair = self.range(string)
            if range_pair:
                return BaseSplitter._split(range_pair, string)
        return string, None

    @staticmethod
    def _split(range_pair, string):
        start, end = range_pair
        length = end - start
        return string[:start], string[start+length:]
    
    def __call__(self, string):
        return self.split(string)

    @abstractmethod
    def range(self, string):
        pass

class RegexSplitter(BaseSplitter):

    def __init__(self, splitter=DEFAULT_REGEX_PATH_DELIMITER):
        super().__init__(splitter)

    def range(self, string):
        match = self.splitter.search(string)
        if match:
            start = match.start()
            end = match.end()
            return start, end

class StringSplitter(BaseSplitter):

    def __init__(self, splitter=DEFAULT_STRING_PATH_DELIMITER):
        super().__init__(splitter)

    def range(self, string):
        start = string.find(self.splitter)
        if start != -1:
            end = start + len(self.splitter)
            return start, end
