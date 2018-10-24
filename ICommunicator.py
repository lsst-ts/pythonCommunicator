from abc import ABC, abstractmethod

class ICommunicator(ABC):
	"""Abstract class to handle different communication protocols.
	----------

	Notes
	-----"""
		
	@abstractmethod
	def connect(self):
		"""Connect
		"""
		pass
		
	@abstractmethod
	def disconnect(self):
		pass
		
	@abstractmethod
	def getMessage(self):
		"""Get message from currect connection 
	
		Returns errorCode, message, errorMessage
		"""
		pass
		
	@abstractmethod
	def sendMessage(self, message):
		"""Send message from currect connection  
	
		Returns errorCode, errorMessage
		"""
		pass
		
	@abstractmethod
	def reconnect(self):
		"""Reconnect 
	
		Returns errorCode, errorMessage
		"""
		pass
		
	@abstractmethod
	def isConnected(self):
		"""Returns an internal parameter to check if it is connected. 
	
		Returns isConnected: True or False
		"""
		pass