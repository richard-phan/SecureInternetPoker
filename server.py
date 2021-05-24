import socket
import os

from utils import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def send_outcomes(socket_list, session_key_list, points):
    if points[0] > points[1]:
        packetWin = encrypt_message(MessageType.WIN.value, session_key_list[0])
        packetLose = encrypt_message(MessageType.LOSE.value, session_key_list[1])
        socket_list[0].send(packetWin)
        socket_list[1].send(packetLose)
    elif points[1] > points[0]:
        packetWin = encrypt_message(MessageType.WIN.value, session_key_list[1])
        packetLose = encrypt_message(MessageType.LOSE.value, session_key_list[0])
        socket_list[1].send(packetWin)
        socket_list[0].send(packetLose)
    else:
        packetTie1 = encrypt_message(MessageType.TIE.value, session_key_list[0])
        packetTie2 = encrypt_message(MessageType.TIE.value, session_key_list[1])
        socket_list[0].send(packetTie1)
        socket_list[1].send(packetTie2)
                

PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('', PORT))
server_socket.listen(2)

while True:
    socket_list = []
    session_key_list = []
    pu_keys = []

    create_keys()
    private_key = RSA.import_key(open('private.pem').read())
    pk_cipher = PKCS1_v1_5.new(private_key)

    while len(socket_list) < 2:
        print('Waiting for connections...')

        main_socket, addr = server_socket.accept()
        socket_list.append(main_socket)

        print('{}:{} has connected'.format(addr[0], addr[1]))

        # receives the public key from the client
        public_key_raw, data_type = recv_msg(main_socket)
        public_key = RSA.import_key(public_key_raw)
        pu_keys.append(public_key)

        # receives the public key from the client
        send_key(main_socket, MessageType.PUBLICKEY)

        enc_session_key = main_socket.recv(128)
        dec_session_key = pk_cipher.decrypt(enc_session_key, 1000)
        session_key_list.append(dec_session_key)

    points = [0 for conn in socket_list]

    for round in range(3):
        for i, connection in enumerate(socket_list):
            nums = generate_numbers(1, 15, 3)
            packet = encrypt_message(nums, session_key_list[i])
            connection.send(packet)

        cards = []
        for i, conn in enumerate(socket_list):
            enc_card = conn.recv(128)
            card = decrypt_message(enc_card, session_key_list[i])
            cards.append(int(card))

        if cards[0] > cards[1]:
            points[0] += 1
        elif cards[1] > cards[0]:
            points[1] += 1

    send_outcomes(socket_list, session_key_list, points)

    socket_list = []
    session_key_list = []
    pu_keys = []

    os.remove('private.pem')
    os.remove('public.pem')