import time
import unittest
from random import randint, choice
from lsst.ts.pythonCommunicator.TcpCommunicator import TcpClient, TcpServer, TCPEndStr, TcpClientAsync, TCPEndStrAsync
import threading
import string
import os
import pty
import serial
import asyncio
from lsst.ts.pythonCommunicator.SerialCommunicator import SerialCommunicator


class TestTCPAsync(unittest.TestCase):

    def setUp(self):
        endStr = "\n"
        maxLength = 1024
        messageHandlerValueAsync = TCPEndStrAsync(endStr, maxLength)
        messageHandlerValue = TCPEndStr(endStr, maxLength)
        address, port, connectTimeout, readTimeout, sendTimeout = "127.0.0.1", 50005, 5, 2, 2
        self.tcpclient = TcpClientAsync(address, port, connectTimeout,
                                        readTimeout, sendTimeout, messageHandler=messageHandlerValueAsync)
        self.tcpserver = TcpServer(address, port, connectTimeout,
                                   readTimeout, sendTimeout, messageHandler=messageHandlerValue)

    def testSimpleEcho(self):
        async def doit():
            for i in range(1, 1023):
                message = ''.join(choice(string.ascii_letters)
                                  for _ in range(i))
                t = threading.Thread(target=echo, args=(self.tcpserver,))
                t.start()
                messageRcvd = await sendMessageEchoAsync(self.tcpclient, message)
                self.assertEqual(message, messageRcvd)
                t.join()
        asyncio.get_event_loop().run_until_complete(doit())

    def tearDown(self):
        async def doit(tcpclient=self.tcpclient):
            await self.tcpclient.disconnect()
            # time.sleep(1)
            # self.tcpserver.disconnect()
        asyncio.get_event_loop().run_until_complete(doit())
        

class TestTCP(unittest.TestCase):

    def setUp(self):
        endStr = "\n"
        maxLength = 1024
        messageHandlerValue = TCPEndStr(endStr, maxLength)
        address, port, connectTimeout, readTimeout, sendTimeout = "127.0.0.1", 50006, 5, 2, 2
        self.tcpclient = TcpClient(address, port, connectTimeout,
                                   readTimeout, sendTimeout, messageHandler=messageHandlerValue)
        self.tcpserver = TcpServer(address, port, connectTimeout,
                                   readTimeout, sendTimeout, messageHandler=messageHandlerValue)

    def testSimpleEcho(self):

        for i in range(1, 1023):
            message = ''.join(choice(string.ascii_letters) for _ in range(i))
            t = threading.Thread(target=echo, args=(self.tcpserver,))
            t.start()
            messageRcvd = sendMessageEcho(self.tcpclient, message)
            self.assertEqual(message, messageRcvd)
            t.join()

    def tearDown(self):
        self.tcpclient.disconnect()
        # time.sleep(1)
        # self.tcpserver.disconnect()


class testSerial(unittest.TestCase):

    def setUp(self):
        self.master, self.slave = pty.openpty()  # Simulate Serial device
        self.s_name = os.ttyname(self.slave)
        self.serialCommunicator = SerialCommunicator(self.s_name, 57600, 'N', stopbits=serial.STOPBITS_ONE,
                                                     bytesize=serial.EIGHTBITS, byteToRead=1024, dsrdtr=False,
                                                     xonxoff=False, timeout=2, termChar="\n",
                                                     delayNextMsg=0.02)
        self.serialCommunicator.connect()

    @unittest.skip("Only test AyncTCP")
    def testMessages(self):
        for i in range(10, 1023):
            message = ''.join(choice(string.ascii_letters) for _ in range(i))
            t = threading.Thread(target=serialEcho, args=(self.master,))
            t.start()
            messageRcvd = sendMessageEcho(self.serialCommunicator, message)
            print("message:" + message)
            print("messageRcvd:" + messageRcvd)
            self.assertEqual(message, messageRcvd)
            t.join()

    def tearDown(self):
        self.serialCommunicator.disconnect()


def echo(tcpserver):
    if tcpserver.isConnected() is False:
        print("Starting echo...")
        tcpserver.connect()
    message = tcpserver.getMessage()
    tcpserver.sendMessage(message)
    return message


async def sendMessageEchoAsync(tcpclient, message):
    if tcpclient.isConnected() is False:
        print("Starting sendMessageEchoAsync...")
        await tcpclient.connect()
    await tcpclient.sendMessage(message)
    message = await tcpclient.getMessage()
    return message


def sendMessageEcho(tcpclient, message):
    if tcpclient.isConnected() is False:
        print("Starting sendMessageEcho...")
        tcpclient.connect()
    tcpclient.sendMessage(message)
    message = tcpclient.getMessage()
    return message


def serialEcho(master):
    message = os.read(master, 1025)
    os.write(master, message)
    return message


if __name__ == '__main__':
    TestTCP = unittest.main()
