from .ICommunicator import ICommunicator
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

    def __init__(self, port, baudrate, parity, stopbits, bytesize, byteToRead=1024, dsrdtr=False, xonxoff=False,
                 timeout=2, termChar="\n"):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopBits = stopbits
        self.byteSize = bytesize
        self.byteToRead = byteToRead
        self.dsrdtr = dsrdtr
        self.xonxoff = xonxoff
        self.timeout = timeout  # read timeout
        self.termChar = termChar

        self.serial = None

    def connect(self):
        """Class to handle Serial connection"""
        try:
            self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopBits, bytesize=self.byteSize, timeout=self.timeout)
            return NOERROR, ""
        except serial.SerialException as e:
            return ERROR, e

    def disconnect(self):
        self.clientSocket.close()

    def getMessage(self):
        try:
            message = self.serial.read(self.byteToRead)
            return NOERROR, message, ""
        except serial.SerialException as e:
            return ERROR, "", e

    def sendMessage(self, message):
        try:
            self.serial.write(message.encode('ascii')+self.termChar)
            return NOERROR, ""
        except serial.SerialException as e:
            return ERROR, e

    def reconnect(self):
        """Reconnect tcp connection"""
        self.disconnect()
        errorCode, errorMsg = self.connect()
        return errorCode, errorMsg

    def isConnected(self):
        return serial.isOpen()


