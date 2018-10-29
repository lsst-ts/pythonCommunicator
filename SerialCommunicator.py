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
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopBits, bytesize=self.byteSize, timeout=self.timeout)

    def disconnect(self):
        self.serial.close()

    def getMessage(self):
        message = self.serial.read(self.byteToRead).decode('ascii')
        return message

    def sendMessage(self, message):
        self.serial.write((message+self.termChar).encode('ascii'))

    def reconnect(self):
        """Reconnect tcp connection"""
        self.disconnect()
        errorCode, errorMsg = self.connect()
        return errorCode, errorMsg

    def isConnected(self):
        return self.serial.isOpen()


