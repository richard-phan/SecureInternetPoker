import os
import socket
import sys

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

sys.path.append('..')
from utils import *

#all this is generation of the public private key
create_keys()

####################################################
# Now let's load those keys

# The public key and the private key
puKey = None
prKey = None

# Load the public key
with open ("private.pem", "rb") as prv_file:
	
	contents = prv_file.read()
	prKey = RSA.importKey(contents)


# Load the public key
with open ("public.pem", "rb") as pub_file:
	contents = pub_file.read()
	puKey = RSA.importKey(contents)


#send over the public key
SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SERVER_IP, SERVER_PORT))

# sends the public key to the server
send_key(client_socket, MessageType.PUBLICKEY)

# receives the public key from the server
public_key_raw, data_type = recv_msg(client_socket)
public_key = RSA.import_key(public_key_raw)
cipher = PKCS1_v1_5.new(public_key)

session_key = get_random_bytes(16)
enc_session_key = cipher.encrypt(session_key)
client_socket.send(enc_session_key)

print('Welcome to Secure Internet Poker')

for i in range(3):
    # gets cards
    enc_data = client_socket.recv(128)
    cards_raw = decrypt_message(enc_data, session_key)
    cards = cards_raw[1:-1].split(', ')
    print('Your cards are:', cards_raw)

    # pick card
    card = None
    while card not in cards:
        card = input('Pick a card: ')
    packet = encrypt_message(card, session_key)
    client_socket.send(packet)
    print('Waiting for other player')


# get win state
enc_state = client_socket.recv(128)
state = decrypt_message(enc_state, session_key)

if state == MessageType.WIN.value:
    print('YOU WON!')
elif state == MessageType.LOSE.value:
    print('YOU LOSE!')
elif state == MessageType.TIE.value:
    print('YOU TIED!')
else:
    print('UNKNOWN')

os.remove('private.pem')
os.remove('public.pem')
