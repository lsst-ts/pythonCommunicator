import socket

def exampleServer():
	TCP_IP = 'localhost'
	TCP_PORT = 5000
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(60)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	
	conn, addr = s.accept()
	print("Connection address:" + str(addr))
	
	data = b'Hello\n'
	print("received data:" + str(data))
	conn.send(data)  # echo
	
	conn.close()

exampleServer()