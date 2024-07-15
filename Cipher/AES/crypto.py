from abc import abstractmethod, ABCMeta

class Crypto(metaclass=ABCMeta):
    @abstractmethod
    def encrypt(self):
        pass
    def decrypt(self):
        pass