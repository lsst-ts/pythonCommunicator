from TcpCommunicator import TcpServerEndChar

print("Accepting connections...")
server = TcpServerEndChar(address="localhost", port=5000)
a, b = server.connect()
error, msg, errorMsg = server.getMessage()
c, d = server.sendMessage("Server: How you doing....\n")

#print(a)
#print(b) 
#print(c)
#print(d) 
print(msg)
print("Program ended")