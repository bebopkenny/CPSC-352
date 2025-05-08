import socket
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import sys

# Ensure user entered four arguments
if len(sys.argv) != 4:
    print("Error. There should be 4 arguments.")
    print("Example: python3 client.py <server IP> <server port> <key>")
    sys.exit(1)

SERVER_IP = sys.argv[1]           # IP
SERVER_PORT = int(sys.argv[2])      # Port
key = sys.argv[3].encode()          # Key

# Checking if the key meets the requirements
if len(key) != 16:
    print("Error: Key must be 16 bytes or 16 characters long! Please try again.")
    sys.exit(1)
    
# Create the client's socket
cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Attempt to connect to the server
cliSock.connect((SERVER_IP, SERVER_PORT))

# Set up the AES encryption with the user key
encCipher = AES.new(key, AES.MODE_ECB)

# Ask user for the message and pad it
message = input("Please enter the message to the server: ").encode()
padded_message = pad(message, 16)

# Encrypt the message
cipherText = encCipher.encrypt(padded_message)

# Send the encrypted message to the server
cliSock.send(cipherText)
print("Encrypted message sent successfully!")

# Close the connection
cliSock.close()
print("Connection closed.")
