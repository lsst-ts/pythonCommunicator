import time
import unittest
from random import randint, choice
from pythonCommunicator.TcpCommunicator import TcpClient, TcpServer, TCPEndStr
import threading
import string
import os, pty, serial
from lsst.ts.pythonCommunicator.SerialCommunicator import SerialCommunicator

class TestTCP(unittest.TestCase):

    def setUp(self):
        endStr = "\n"
        maxLength = 1024
        messageHandlerValue = TCPEndStr(endStr, maxLength)
        address, port, connectTimeout, readTimeout, sendTimeout = "localhost", 50001, 2, 2, 2 
        self.tcpclient = TcpClient(address, port, connectTimeout, readTimeout, sendTimeout, messageHandler=messageHandlerValue)
        self.tcpserver = TcpServer(address, port, connectTimeout, readTimeout, sendTimeout, messageHandler=messageHandlerValue)

    #@unittest.skip("Only test serial")
    def testSimpleEcho(self):
        
        for i in range(1,1023):
            message = ''.join(choice(string.ascii_letters) for _ in range(i))
            t = threading.Thread( target=echo, args=(self.tcpserver,) )
            t.start()
            messageRcvd = sendMessageEcho(self.tcpclient, message)
            self.assertEqual(message, messageRcvd)
            t.join()

    def tearDown(self):
        self.tcpclient.disconnect()
        #self.tcpserver.disconnect()
        pass

class testSerial(unittest.TestCase):

    def setUp(self):
        self.master, self.slave = pty.openpty() #Simulate Serial device
        self.s_name = os.ttyname(self.slave)
        self.serialCommunicator = SerialCommunicator(self.s_name, 57600, 'N', stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, byteToRead=1024, dsrdtr=False, xonxoff=False, timeout=2, termChar="\n", delayNextMsg=0.02)
        self.serialCommunicator.connect()

    def testMessages(self):
        for i in range(10,1023):
            message = ''.join(choice(string.ascii_letters) for _ in range(i))
            t = threading.Thread( target=serialEcho, args=(self.master,) )
            t.start()
            messageRcvd = sendMessageEcho(self.serialCommunicator, message)
            print("message:" + message)
            print("messageRcvd:" + messageRcvd)
            self.assertEqual(message, messageRcvd)
            t.join()

    def tearDown(self):
        self.serialCommunicator.disconnect()

def echo(tcpserver):
    print("Starting echo...")
    if tcpserver.isConnected() == False:
        tcpserver.connect()
    message = tcpserver.getMessage()
    tcpserver.sendMessage(message)
    print("Stopping server...")
    return message

def sendMessageEcho(tcpclient, message):
    print("Starting sendMessageEcho...")
    if tcpclient.isConnected() == False:
        tcpclient.connect()
    tcpclient.sendMessage(message)
    message = tcpclient.getMessage()
    print("Stopping server...")

    return message

def serialEcho(master):
    message = os.read(master,1025)
    os.write(master, message)

    return message

if __name__ == '__main__':
    TestTCP = unittest.main()
