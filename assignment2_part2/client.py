import socket
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Hash import SHA256
import Cryptodome.Signature.pkcs1_15 
from Cryptodome.PublicKey import RSA
import struct
import sys

# Function to create the message to a SHA256 and signs it with the private key
def sign_message(message): 
    hash = SHA256.new(message)
    PRIVATE_KEY_FILE_NAME = "private-key.pem"
    privKey = RSA.import_key(open(PRIVATE_KEY_FILE_NAME).read())
    sig1 = Cryptodome.Signature.pkcs1_15.new(privKey)
    signature = sig1.sign(hash)
    return signature
    
if len(sys.argv) != 4:
    print("Error. There should be 4 arguments.")
    print("Example: python3 client.py <server IP> <server port> <key>")
    sys.exit(1)

SERVER_IP = sys.argv[1]           # IP
SERVER_PORT = int(sys.argv[2])      # Port
key = sys.argv[3].encode()          # Key

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

# Sign the original raw message to make it a SHA256 and sign it with private key
signature = sign_message(message)

# Encrypt the padded message
cipherText = encCipher.encrypt(padded_message)

# Payload Construction
# 1. A 4 byte header that indicates the length of the signature
# 2. The RSA signature
# 3. The AES encrypted cipher text of the padded message
signature_length = len(signature)
header = struct.pack("!I", signature_length)
payload = signature + header + cipherText

# Send the encrypted message to the server
cliSock.send(payload)
print("Encrypted message sent successfully!")

# Close the connection
cliSock.close()
print("Connection closed.")
