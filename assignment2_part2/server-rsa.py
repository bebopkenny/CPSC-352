import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import struct
import sys

# Importing the public key
PUBLIC_KEY_FILE_NAME = "public-key.pem"
# Load public key
pubKey = RSA.import_key(open(PUBLIC_KEY_FILE_NAME).read())

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
    cliMsg = cliSock.recv(4096)
    if not cliMsg:
        print("Error: received an empty message. Program will now close.")
        cliSock.close()
        continue
    
    print(f"Encrypted message received: {cliMsg.hex()}")
    
    # Extract the first 4 bytes 
    header = cliMsg[:4]
    
    # Unpack the message to get the length of the signature
    sig_length = struct.unpack("!I", header)[0] # The "!I" means big-endian
    
    signature = cliMsg[4:4+sig_length]

    # Extract the remainder of the payload as ciphertext
    cipherText = cliMsg[4+sig_length:]
    
    # Decrypt the ciphertext using AES 
    decCipher = AES.new(client_key, AES.MODE_ECB)
    padded_plaintext = decCipher.decrypt(cipherText)
    
    try:
        plaintext = unpad(padded_plaintext, 16)
    except Exception as e:
        print(f"Unpadding failed: {e}")
        cliSock.close()
        continue
    
    # Verify the signature against the decrypted plaintext
    message_hash = SHA256.new(plaintext)
    try:
        pkcs1_15.new(pubKey).verify(message_hash, signature)
        print("Signature is valid")
    except ValueError:
        print("Signature validation failed!")
        
    print(f"Decrypted message: {plaintext.decode('utf-8')}" )
    cliSock.close()
    print("Client disconnected, waiting for next connection...")