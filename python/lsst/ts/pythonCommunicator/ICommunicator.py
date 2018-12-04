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
	
		Returns message
		"""
		pass
		
	@abstractmethod
	def sendMessage(self, message):
		"""Send message from current connection  
	
		Returns 
		"""
		pass
		
	@abstractmethod
	def reconnect(self):
		"""Reconnect 
	
		Returns 
		"""
		pass
		
	@abstractmethod
	def command(self, commandMessage):
		"""Send message from currect connection  
	
		Returns command response
		"""
		pass
		
	@abstractmethod
	def isConnected(self):
		"""Returns an internal parameter to check if it is connected. 
	
		Returns isConnected: True or False
		"""
		pass