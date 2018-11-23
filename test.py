import time
import unittest
from random import randint, choice
from pythonCommunicator.TcpCommunicator import TcpClient, TcpServer, TCPEndStr
import threading
import string

# testClass = TcpClient(address="192.168.0.1", port=5000)
# a, b = testClass.connect()
# testClass.disconnect()

class TestTCP(unittest.TestCase):

    def setUp(self):
        endStr = "\n"
        maxLength = 1024
        messageHandlerValue = TCPEndStr(endStr, maxLength)
        address, port, connectTimeout, readTimeout, sendTimeout = "localhost", 50001, 2, 2, 2 
        self.tcpclient = TcpClient(address, port, connectTimeout, readTimeout, sendTimeout, messageHandler=messageHandlerValue)
        self.tcpserver = TcpServer(address, port, connectTimeout, readTimeout, sendTimeout, messageHandler=messageHandlerValue)

    def testSimpleEcho(self):
        
        for i in range(10,1023):
            message = ''.join(choice(string.ascii_letters) for _ in range(i))
            t = threading.Thread( target=echo, args=(self.tcpserver,) )
            t.start()
            messageRcvd = sendMessageEcho(self.tcpclient, message)
            self.assertEqual(message, messageRcvd)
            t.join()

    def tearDown(self):
        self.tcpclient.disconnect()
        self.tcpserver.disconnect()
        pass
    
def echo(tcpserver):
    print("Starting echo...")
    if tcpserver.connected == False:
        tcpserver.connect()
    message = tcpserver.getMessage()
    tcpserver.sendMessage(message)
    print("Stopping server...")
    return message

def sendMessageEcho(tcpclient, message):
    print("Starting sendMessageEcho...")
    if tcpclient.connected == False:
        tcpclient.connect()
    tcpclient.sendMessage(message)
    message = tcpclient.getMessage()
    print("Stopping server...")

    return message

if __name__ == '__main__':
    TestTCP = unittest.main()
