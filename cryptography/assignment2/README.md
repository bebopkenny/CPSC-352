# **AES Encrypted Client-Server Communication**  

This program demonstrates encrypted message transmission between a client and a server using **AES encryption** (Advanced Encryption Standard). It allows a client to send an **encrypted message**, which the server will **decrypt and print**.  

## **Features**
- Users can define their **own IP, port, and encryption key** via command-line arguments.
- Messages are **encrypted** before being sent to the server.
- The server **decrypts** and displays the original message.
- Multiple clients can send messages to the same server **if they provide the correct port and key**.

---

## **Installation**  
Before running the program, ensure that all necessary dependencies are installed.

### **Linux Users** 🐧  
Run the following commands in your terminal:  
```bash
sudo apt update && sudo apt install python3-pip -y
pip install -r requirements.txt
```

### **Mac Users** 🍏
Run:
```bash
brew install python3
pip3 install -r requirements.txt
```
## **Running the Program**

### 1. Start the Server

First, launch the server before running the client. Replace `<port>` and `<key>` with your desired values (16-byte key required):

```bash
python3 server.py <port> <key>
```
**Example:** 
```bash
python3 server.py 1234 abcdefghnbfghasd
```
### 2. Start the Client
Once the server is running, launch the client in another terminal. The client must match the server's IP, port, and encryption key:
```bash
python3 client.py <server IP> <server port> <key>
```
**Example:**
```bash
python3 client.py 127.0.0.1 1234 abcdefghnbfghasd
```
### 3. Enter Your Message ###
The client will prompt you to enter a message. The message is automatically encrypted and sent to the server. The server decrypts the message and displays the original text.

### Notes ###
- The server must be running before a client can send a message.
- The key must be exactly 16 bytes long, or the encryption will fail.
- AES is a block cipher that encrypts messages in 16-byte blocks, so messages are padded if needed.