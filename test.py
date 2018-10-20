from TcpCommunicator import TcpClient, TcpClienEndChar

# testClass = TcpClient(address="192.168.0.1", port=5000)
# a, b = testClass.connect()
# testClass.disconnect()

testClass2 = TcpClienEndChar(address="localhost", port=5000)
a, b = testClass2.connect()
error, message, errorMsg = testClass2.getMessage()
print(str(message))
print(repr(errorMsg))
testClass2.disconnect()

print(b)
print("All good")