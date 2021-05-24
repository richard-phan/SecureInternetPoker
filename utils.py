import random
from enum import Enum
from Crypto.PublicKey import RSA
from Crypto.Util import Padding
from Crypto.Cipher import AES

HEADER_LENGTH = 10

class MessageType(Enum):
    MESSAGE = '0'
    CARDS = '1'
    CHOICE = '2'
    TURN = '3'
    WIN = '4'
    LOSE = '5'
    TIE = '6'
    END = '7'
    PUBLICKEY = '8'
    AES = '9'

def create_keys():
    # Generate a public/private key pair
    private_key = RSA.generate(bits=1024)

    # Get the private key
    public_key = private_key.publickey()

    # The private key bytes to print
    privKeyBytes = private_key.exportKey(format='PEM') 

    # The public key bytes to print
    pubKeyBytes = public_key.exportKey(format='PEM') 

    # Save the private key
    with open ("private.pem", "wb") as prv_file:
        prv_file.write(privKeyBytes)

    # Save the public key
    with open ("public.pem", "wb") as pub_file:
        pub_file.write(pubKeyBytes)

def send_key(socket, msg_type):
    file = 'private.pem'
    if msg_type == MessageType.PUBLICKEY:
        file = 'public.pem'

    pub_key = open(file, 'r').read()
    packet = create_packet(pub_key, msg_type)
    socket.send(packet)

def encrypt_message(msg, session_key):
    cipher = AES.new(session_key, AES.MODE_ECB)
    data = Padding.pad(msg.encode(), 16)
    return cipher.encrypt(data)

def decrypt_message(msg, session_key):
    cipher = AES.new(session_key, AES.MODE_ECB)
    data = cipher.decrypt(msg)
    return Padding.unpad(data, 16).decode()

def create_packet(data, data_type):
    data_len = str(len(data))
    padding = len(data_len)
    return ('0' * (HEADER_LENGTH - padding - 1) + data_len + data_type.value + data).encode('utf-8')

def sendMsg(sock, msg):

	# Get the message length
	msgLen = str(len(msg))
	
	# Keep prepending 0's until we get a header of 3	
	while len(msgLen) < 3:
		msgLen = "0" + msgLen
	
	# Encode the message into bytes
	msgLen = msgLen.encode()
	
	# Put together a message
	sMsg = msgLen + msg
	
	# Send the message
	sock.sendall(sMsg)

def recvMsg(sock):
	
	# The size
	size = sock.recv(3)
	
	# Convert the size to the integer
	intSize = int(size)

	# Receive the data
	data = sock.recv(intSize)

	return data

def recv_msg(socket):
    header = socket.recv(HEADER_LENGTH).decode('utf-8')
    data_len = int(header[:9])
    data_raw = socket.recv(data_len)
    return data_raw.decode('utf-8'), header[9:]

def generate_numbers(start, end, amount):
    nums = []
    for i in range(amount):
        nums.append(random.randint(start, end))
    
    return str(nums)