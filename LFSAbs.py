from abc             import ABC
from abc             import abstractmethod

class LFSAbs(ABC):
    @abstractmethod
    def buildDistro(self): pass
