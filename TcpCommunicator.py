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
	def __init__(self, address, port, connectTimeout=2, readTimeout=2, sendTimeout=2):
		self.address = address
		self.port = port
		self.connectTimeout = connectTimeout
		self.readTimeout = readTimeout
		self.sendTimeout = sendTimeout
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected = False 

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

	def command(self, commandMessage):
		pass
		
	def sendMessage(self, message):
		self.clientSocket.settimeout(self.sendTimeout)
		
	def reconnect(self):
		"""Reconnect tcp connection
		"""
		self.disconnect()
		self.connect()
		
	def isConnected(self):
		return self.connected
		
class TcpClientEndChar(TcpClient):

	def __init__(self, address, port, connectTimeout=2, readTimeout=2, sendTimeout=2, endStr='\n', maxLength = 1024):
		super().__init__(address, port, connectTimeout, readTimeout, sendTimeout)
		self.endStr = endStr
		self.maxLength = maxLength
		
	def getMessage(self):
		"""Placeholder to get message"""
		super().getMessage()
		endStrLen = len(self.endStr)
		message = ""
		OK = False
		for i in range(self.maxLength):
			lastMsg = self.clientSocket.recv(endStrLen).decode("latin-1", errors='replace')
			if(lastMsg == self.endStr):
				OK = True
				break
			message += lastMsg
		if(OK == True):
			print(message)
			return message
		else:
			raise ValueError('End message not found.')

	def command(self, commandMessage):
		self.sendMessage(commandMessage)
		response = self.getMessage()
		return response
		
	def sendMessage(self, message):
		"""Placeholder to send message"""
		internalMessage = (message+self.endStr).encode('utf8')
		super().sendMessage(internalMessage)
		print(internalMessage)
		self.clientSocket.send(internalMessage)
			
			
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
	def __init__(self, address, port, connectTimeout=600, readTimeout=2, sendTimeout=2):
		self.address = address
		self.port = port
		self.connectTimeout = connectTimeout
		self.readTimeout = readTimeout
		self.sendTimeout = sendTimeout
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

	def command(self, commandMessage):
		pass
		
	def disconnect(self):
		"""Disconnect from server"""
		self.connected = False
		self.connection.close()
		
	def getMessage(self):
		"""Placeholder to get message"""
		self.connection.settimeout(self.readTimeout)

		
	def sendMessage(self, message):
		"""Placeholder to send message"""
		self.connection.settimeout(self.sendTimeout)
		
	def reconnect(self):
		self.disconnect()
		self.connect()

	def isConnected(self):
		return self.connected
		
class TcpServerEndChar(TcpServer):

	def __init__(self, address, port, connectTimeout=600, readTimeout=2, sendTimeout=2, endStr="\n", maxLength = 1024):
		super().__init__(address, port, connectTimeout, readTimeout, sendTimeout)
		self.endStr = endStr
		self.maxLength = maxLength
		
	def getMessage(self):
		super().getMessage()
		endStrLen = len(self.endStr)
		message = ""
		OK = False

		for i in range(self.maxLength):
			lastMsg = self.connection.recv(endStrLen).decode("latin-1") 
			message += lastMsg
			if(lastMsg == self.endStr):
				OK = True
				break
		if(OK == True):
			return message

		return message
			
	def sendMessage(self, message):
		internalMessage = message
		super().sendMessage(internalMessage)
		self.connection.send(internalMessage)
