# Assignment 2 Part 2 - Digital Signatures with AES Encryption

This project implements two versions of a secure client/server system that sends encrypted messages with appended digital signatures. One version uses RSA-based digital signatures, and the other uses DSA-based digital signatures. The message itself is encrypted with AES (in ECB mode) using a 16-byte key provided by the user.

## Files in This Directory

- `client-rsa.py`: RSA client – signs messages with an RSA private key, encrypts them with AES, and sends the payload.
- `server-rsa.py`: RSA server – receives the payload, decrypts it with AES, and verifies the RSA signature using the RSA public key.
- `client-dsa.py`: DSA client – signs messages with a DSA private key, encrypts them with AES, and sends the payload.
- `server-dsa.py`: DSA server – receives the payload, decrypts it with AES, and verifies the DSA signature using the DSA public key.
- `requirements.txt`: Contains the library needed to run the program.
- `README.md`: This file.

## Installation

Make sure you have Python 3 installed. Then, to install the required libraries, open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

## How It works

Both versions follow a similar approach:

1. The client reads a message from the user.
2. The client pads and encrypts the message using AES with a 16-byte key.
3. The client digitally signs the original unpadded message.
4. A payload is constructed: a 4-byte header (indicating the signature length), the signature, and the ciphertext.
5. The server receives the payload, extracts the header to determine the signature length, then the signature, and the AES ciphertext.
6. The server decrypts the ciphertext using the AES key, removes the padding, and verifies the digital signature using the corresponding public key.

## How to Run the Programs

Open a terminal in the project directory. The following instructions assume that you have the same directory structure as shown below:

```ruby
bebopkenny@DESKTOP-RPRFOE6:~/CPSC-352/assignment2_part2$ ls
README.md  client-dsa.py  client-rsa.py  requirements.txt  server-dsa.py  server-rsa.py
```
## Running the RSA Version
1. **Start the RSA Server:**

In one terminal window, run:
```bash
python3 server-rsa.py <port> <AES key>
```
For example:
```bash
python3 server-rsa.py 1234 abcdefghnbfghasd
```
Note:  Replace ```<port>``` with the desired port number and ```<AES key>``` with a 16-character key.

2. **Start teh RSA Client:**

In another terminal window, run:
```bash
python3 client-rsa.py <server IP> <server port> <AES key>
```
For example:
```bash
python3 client-rsa.py 127.0.0.1 1234 abcdefghnbfghasd
```
Then, follow the prompt to enter the message you want to send.

## Running the DSA Version
1. **Start the DSA Server**

In one terminal window, run:
```bash
python3 server-dsa.py <port> <AES key>
```
For example:
```bash
python3 server-dsa.py 1234 abcdefghnbfghasd
```
2. **Start the DSA Client:**
In another terminal window, run:
```bash
python3 client-dsa.py <server IP> <server port> <AES key>
```
For example:
```bash
python3 client-dsa.py 127.0.0.1 1234 abcdefghnbfghasd
```
Then, follow the prompt to enter the message you want to send.

## Notes
- **AES Key:**

    The AES key provided must be exactly 16 bytes (16 characters) long.
- **Digital Signature:**
    For RSA, the client signs using its RSA private key and the server verifies with the RSA public key. For DSA, the client signs using its DSA private key and the server verifies with the DSA public key.
- **Payload Structure:**
    
    Both versions construct the payload as follows:   
    - 4-byte header indicating the length of the signature.
    - The digital signature.
    - The AES-encrypted ciphertext.
---
Feel free to reach out if you have any questions about the implementation.


