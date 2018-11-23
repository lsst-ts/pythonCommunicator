from pythonCommunicator.ICommunicator import ICommunicator
import socket

class TcpClient(ICommunicator):
	"""Class to handle TCP connection
	----------
	address : ``string``
		Address of the TCP server
	port : `int` 
		Port to connect to the TCP Server
	connectTimeout : `int` 
		Timeout to connect to the TCP server
	readTimeout : `int` 
		Timeout to read messages from the TCP server
	sendTimeout : `int` 
		Timeout to send messages to the TCP server
	Notes """
	def __init__(self, address, port, connectTimeout=2, readTimeout=2, sendTimeout=2, messageHandler = None):
		self.address = address
		self.port = port
		self.connectTimeout = connectTimeout
		self.readTimeout = readTimeout
		self.sendTimeout = sendTimeout
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected = False

		self.messageHandler = TCPEndStr(endStr='\n', maxLength=1024) if messageHandler is None else messageHandler

	def connect(self):
		"""Class to handle TCP connection
		"""
		self.clientSocket.settimeout(self.connectTimeout)
		self.clientSocket.connect((self.address, self.port))
		self.connected = True 

	def disconnect(self):
		self.connected = False
		self.clientSocket.close()
		
	def getMessage(self):
		self.clientSocket.settimeout(self.readTimeout)
		message = self.messageHandler.getMessage(connection=self.clientSocket)
		return message

	def command(self, commandMessage):
		self.clientSocket.settimeout(self.sendTimeout)
		self.messageHandler.sendMessage(connection=self.clientSocket, message=commandMessage)
		message = self.messageHandler.getMessage(connection=self.clientSocket)
		return message
		
	def sendMessage(self, message):
		self.clientSocket.settimeout(self.sendTimeout)
		self.messageHandler.sendMessage(connection=self.clientSocket, message=message)

	def reconnect(self):
		"""Reconnect tcp connection
		"""
		self.disconnect()
		self.connect()
		
	def isConnected(self):
		return self.connected


class TcpServer(ICommunicator):
	"""Class to handle TCP Server connection, connect will listen (connectionTimeout seconds) until connects to the server
	----------
	address : ``string``
		Address of the TCP server
	port : `int`
		Port to connect to the TCP Server
	connectTimeout : `int`
		Timeout to connect to the TCP server
	readTimeout : `int`
		Timeout to read messages from the TCP server
	sendTimeout : `int`
		Timeout to send messages to the TCP server
	Notes """

	def __init__(self, address, port, connectTimeout=600, readTimeout=2, sendTimeout=2, messageHandler = None):
		self.address = address
		self.port = port
		self.connectTimeout = connectTimeout
		self.readTimeout = readTimeout
		self.sendTimeout = sendTimeout

		self.messageHandler = TCPEndStr(endStr='\n', maxLength=1024) if messageHandler is None else messageHandler

		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection = 0
		self.client_address = ""
		self.connected = False

	def connect(self):
		"""Class to handle TCP connection

		"""
		self.serverSocket.settimeout(self.connectTimeout)
		self.serverSocket.bind((self.address, self.port))
		self.serverSocket.listen(1)
		self.connection, self.client_address = self.serverSocket.accept()
		self.connected = True

	def disconnect(self):
		"""Disconnect from server"""
		self.connected = False
		self.connection.close()
		self.serverSocket.close()

	def getMessage(self):
		self.connection.settimeout(self.readTimeout)
		message = self.messageHandler.getMessage(connection=self.connection)
		return message

	def command(self, commandMessage):
		self.connection.settimeout(self.sendTimeout)
		self.messageHandler.sendMessage(connection=self.connection, message=commandMessage)
		message = self.messageHandler.getMessage(connection=self.connection)
		return message

	def sendMessage(self, message):
		self.connection.settimeout(self.sendTimeout)
		self.messageHandler.sendMessage(connection=self.connection, message=message)

	def reconnect(self):
		self.disconnect()
		self.connect()

	def isConnected(self):
		return self.connected


class MessageHandler:
	"""Class to handle different types of communication"""

	def __init__(self):
		pass

	def getMessage(self, connection):
		raise Exception("MessageHandler hasn't been defined")

	def sendMessage(self, connection, message):
		raise Exception("MessageHandler hasn't been defined")

class TCPEndStr(MessageHandler):
	"""Class to handle different types of communication"""

	def __init__(self, endStr='\n', maxLength=1024):
		self.maxLength = maxLength
		self.endStr = endStr

	def getMessage(self, connection):
		"""Placeholder to get message"""
		endStrLen = len(self.endStr)
		message = ""
		OK = False
		for i in range(self.maxLength):
			lastMsg = connection.recv(endStrLen).decode("latin-1", errors='replace')
			messageAux = message+lastMsg
			if(messageAux.endswith(self.endStr)):
				OK = True
				break
			message = messageAux
		if(OK == True):
			print(message)
			return message
		else:
			raise ValueError('End message not found.')

	def sendMessage(self, connection, message):
		"""Placeholder to send message"""
		internalMessage = (message+self.endStr).encode("latin-1")
		print(internalMessage)
		connection.send(internalMessage)
