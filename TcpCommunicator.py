from ICommunicator import ICommunicator
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

	def connect(self):
		"""Class to handle TCP connection
	
		Returns error code:
		0: Succesfully connected
		-1: Couldn't connect 
		"""
		try:
			self.clientSocket.settimeout(self.connectTimeout)
			self.clientSocket.connect((self.address, self.port))
			return 0, ""
		except socket.error as e:
			#print("Couldn't connect with the socket-server: "+str(e))
			return -1, e

	def disconnect(self):
		"""Disconnect from server"""
		self.clientSocket.close()
		
	def getMessage(self):
		"""Placeholder to get message"""
		self.clientSocket.settimeout(self.readTimeout)

		
	def sendMessage(self, message):
		"""Placeholder to send message"""
		self.clientSocket.settimeout(self.sendTimeout)
		
	def reconnect(self):
		"""Reconnect tcp connection
	
		Returns error code:
		0: Succesfully connected
		-1: Couldn't connect 
		"""
		self.disconnect()
		errorCode, errorMsg = self.connect()
		return errorCode, errorMsg
		
class TcpClienEndChar(TcpClient):

	def __init__(self, address, port, connectTimeout=2, readTimeout=2, sendTimeout=2, endStr="\n", maxLength = 1024):
		super().__init__(address, port, connectTimeout, readTimeout, sendTimeout)
		self.endStr = endStr
		self.maxLength = maxLength
		
	def getMessage(self):
		"""Placeholder to get message"""
		super().getMessage()
		endStrLen = len(self.endStr)
		print(endStrLen)
		message = ""
		OK = -1
		try:
			
			for i in range(self.maxLength):
				lastMsg = self.clientSocket.recv(endStrLen).decode("utf-8") 
				message += lastMsg
				if(lastMsg == self.endStr):
					OK = 0
					break
			if(OK == -1):
				return OK, message, "Message not ended"
			if(OK == 0):
				return 0, message, ""
				
		except socket.error as e:
			#print("Couldn't connect with the socket-server: "+str(e))
			return -1, "", e
			
		return -1, message, "Message not ended"
			
	def sendMessage(self, message):
		"""Placeholder to send message"""
		super().sendMessage()
		try:
			self.clientSocket.send(message)
			return 0, ""
		except socket.error as e:
			#print("Couldn't connect with the socket-server: "+str(e))
			return -1, e