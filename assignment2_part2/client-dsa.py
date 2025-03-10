import socket
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import DSA
from Cryptodome.Signature import DSS
import struct
import sys

# Command line must have four arguments
if len(sys.argv) != 4:
    print("Error. There should be 4 arguments.")
    print("Example: python3 client.py <server IP> <server port> <key>")
    sys.exit(1)

SERVER_IP = sys.argv[1] # IP
SERVER_PORT = int(sys.argv[2]) # Port
aes_key = sys.argv[3].encode()# Key

# Checking if the key is 16 bytes or 16 characters long
if len(aes_key) != 16:
    print("Error: Key must be 16 bytes or 16 characters long! Please try again.")
    sys.exit(1)

# Load your existing DSA private key (generated beforehand)
try:
    with open("dsa_private_key.pem", "rb") as f:
        dsa_key = DSA.import_key(f.read())
except FileNotFoundError:
    print("Error: dsa_private_key.pem not found. Please generate it first.")
    sys.exit(1)

# Create the client's socket and connect to the server
cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliSock.connect((SERVER_IP, SERVER_PORT))

# Set up the AES encryption with the user key
encCipher = AES.new(aes_key, AES.MODE_ECB)

# Ask user for the message and pad it for AES encryption
message = input("Please enter the message to the server: ").encode()
padded_message = pad(message, 16)

# Sign the original raw message NOT the padded version
hash_obj = SHA256.new(message)
signer = DSS.new(dsa_key, 'fips-186-3')
signature = signer.sign(hash_obj)

# Encrypt the padded message with AES
cipherText = encCipher.encrypt(padded_message)

# Payload Construction:
# 1. A 4-byte header that indicates the length of the signature
# 2. The RSA signature
# 3. The AES encrypted cipher text of the padded message
sig_length = len(signature)
header = struct.pack("!I", sig_length) 
payload = header + signature + cipherText

# Send the payload to the server
cliSock.send(payload)
print("Encrypted message with DSA signature sent successfully!")

# Close the connection
cliSock.close()
print("Connection closed.")
