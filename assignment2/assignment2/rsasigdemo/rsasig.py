from Cryptodome.PublicKey import RSA
from Cryptodome.Signature.pkcs1_15 import PKCS115_SigScheme
from Cryptodome.Hash import SHA256
import binascii
import Cryptodome.Signature.pkcs1_15 

########## Load the public and private keys from files ##############

# The plaintext bytes
plainBytes = b'This is a test!'

# The name of the public key file
PUBLIC_KEY_FILE_NAME = "public-key.pem"

# Private key file name
PRIVATE_KEY_FILE_NAME = "private-key.pem"

# Load the public key
pubKey = RSA.import_key(open(PUBLIC_KEY_FILE_NAME).read())

# Load the private key
privKey = RSA.import_key(open(PRIVATE_KEY_FILE_NAME).read())

###############################################################
# If you want to randomly generate keys instead of loading 
# pre-generated keys from files, uncomment this.
# Generate 1024-bit RSA key pair (private + public key)
#keyPair = RSA.generate(bits=1024)
# Get just the public key
#justPubKey = keyPair.publickey()
################################################################

# The good message
msg = b'hello'

# The tempered message
msg1 = b'tempered'

# Compute the hashes of both messages
hash = SHA256.new(msg)
hash1 = SHA256.new(msg1)

# Sign the hash
sig1 = Cryptodome.Signature.pkcs1_15.new(privKey)
signature = sig1.sign(hash)

##################### On the arrival side #########################

# Note, we will have to take the decrypted message, hash it and then provide the hash and the signature to the 
# verify function

verifier = Cryptodome.Signature.pkcs1_15.new(pubKey)

# If the verification succeeds, nothing is returned.  Otherwise a ValueError exception is raised
# Let's try this with the valid message
try:
    verifier.verify(hash, signature)
    print("The signature is valid!")
except ValueError:    
    print("The signature is not valid!")


