from ICommunicator import ICommunicator
import serial

NOERROR = 0
ERROR = -1

class SerialCommunicator(ICommunicator):
	"""Class to handle TCP connection
	----------
	port : `string` 
	baudrate : `int` 
	parity : `int` 
	stopbits : `int` 
	bytesize : `int` 
	timeout : `int
	bytesToRead : `int
	Notes """
	def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout, byteToRead=1):
		self.port = port
		self.baudrate = baudrate
		self.parity = parity
		self.stopBits = stopBits
		self.byteSize = byteSize
		self.byteToRead = byteToRead
		self.serial = serial.Serial()
		
	def connect(self):
		"""Class to handle Serial connection
		"""
		try:
			self.serial = serial.Serial(self.port, self.baudrate, self.parity, self.stopbits, self.bytesize)
			return NOERROR, ""
		except serial.SerialException as e:
			return ERROR, e

	def disconnect(self):
		self.clientSocket.close()
		
	def getMessage(self):
		pass

		
	def sendMessage(self, message):
		pass
		
	def reconnect(self):
		"""Reconnect tcp connection
		"""
		self.disconnect()
		errorCode, errorMsg = self.connect()
		return errorCode, errorMsg
		
	def isConnected(self):
		return serial.isOpen()
		
class SerialCommunicatorEndChar(SerialCommunicator):

	def __init__(self, port, baudrate, parity, stopbits, bytesize, byteToRead=1):
		super.__init__(port, baudrate, parity, stopbits, bytesize, byteToRead)
		
	def getMessage(self):
		try:
			message = self.serial.read(self.byteToRead)
			return NOERROR, message, ""
		except serial.SerialException as e:
			return ERROR, "", e		

	def sendMessage(self, message):
		try:
			self.serial.write(message.encode('ascii'))
			return NOERROR, ""
		except serial.SerialException as e:
			return ERROR, e			
		
