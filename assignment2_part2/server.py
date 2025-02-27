import socket
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import sys

# Importing the public key
PUBLIC_KEY_FILE_NAME = "public-key.pem"

if len(sys.argv) != 3:
    print("Error. Command line must have three arguments.")
    print("Example: python3 server.py <port number> <16-byte key>")
    sys.exit(1)

PORT_NUMBER = int(sys.argv[1])
client_key = sys.argv[2].encode()

if len(client_key) != 16:
    print("Error: Key must be 16 bytes or 16 characters long! Please try again.")
    sys.exit(1)
    
# Create a socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associate the socket with the port
serverSock.bind(('', PORT_NUMBER))

# Start listening for incoming connections
serverSock.listen(100)
print(f"Server is listening on port {PORT_NUMBER}")

while True:
    print("Waiting for connection...")
    cliSock, cliInfo = serverSock.accept()  # Accept connection
    print(f"Client connected from {cliInfo}")

    # Receive encrypted message 
    cliMsg = cliSock.recv(1024)
    if not cliMsg:
        print("Error: received an empty message. Program will now close.")
        cliSock.close()
        continue
    
    print(f"Encrypted message received: {cliMsg.hex()}")
    
    try:
        decCipher = AES.new(client_key, AES.MODE_ECB)
        decrypted_message = unpad(decCipher.decrypt(cliMsg), 16).decode()
        print(f"Decrypted message: {decrypted_message}")
    except Exception as e:
        print(f"Decryption failed: {e}")
        
    cliSock.close()
    print("Client disconnected, waiting for next connection...")
