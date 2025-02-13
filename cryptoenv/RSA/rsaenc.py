from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import sys


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


############# ENCRYPTION ###############


# Create an instance of the RSA encryption class
# that will be used for encrypting with the public
# key
cipher_rsa_encrypt = PKCS1_OAEP.new(pubKey, hashAlgo=None, mgfunc=None, randfunc=None)


	
# Encrypt!
cipherBytes = cipher_rsa_encrypt.encrypt(plainBytes)
		
############# DECRYPTION ###################	


# Create an instance of the RSA decryption class 
# that will be used for encrypting with the public
# key
cipher_rsa_decrypt = PKCS1_OAEP.new(privKey, hashAlgo=None, mgfunc=None, randfunc=None)


# Decrypt!
decryptedBytes = cipher_rsa_decrypt.decrypt(cipherBytes)


########### Print the results ################
print("Original bytes: ", plainBytes)
print("")


print("Encrypted bytes: ", cipherBytes)
print("")


print("Decrypted bytes: ", decryptedBytes)