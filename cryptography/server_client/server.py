import socket

####### A SIMPLE ILLUSTRATION OF THE TCP SERVER #######

# The port number on which to listen for incoming
# connections.
PORT_NUMBER = 1235

# Create a socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Associate the socket with the port
serverSock.bind(('', PORT_NUMBER)) 

# Start listening for incoming connections (we can have
# at most 100 connections waiting to be accepted before
# the server starts rejecting new connections)
serverSock.listen(100)

# Keep accepting connections forever
while True:

	print("Waiting for clients to connect...")
	
	# Accept a waiting connection
	cliSock, cliInfo = serverSock.accept()
	
	print("Client connected from: " + str(cliInfo))
	
	# Receive the data the client has to send.
	# This will receive at most 1024 bytes
	cliMsg = cliSock.recv(1024)
	
	# The string containing the uppercased message
	upperMsgStr = cliMsg.decode().upper()
	
	print("Client sent " + str(cliMsg.decode()))

	# Send the upper-cased string back to the client
	cliSock.send(upperMsgStr.encode())
	
	# Hang up the client's connection
	cliSock.close()
