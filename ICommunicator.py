from abc import ABC, abstractmethod

class ICommunicator(ABC):
    """Abstract class to handle different communication protocols. 
    ----------

    Notes
    -----"""
		
    @abstractmethod
    def connect(self):
        pass
		
    @abstractmethod
    def disconnect(self):
        pass
		
    @abstractmethod
    def getMessage(self):
        pass
		
    @abstractmethod
    def sendMessage(self, message):
        pass
		
    @abstractmethod
    def reconnect(self):
        pass