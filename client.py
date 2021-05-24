import socket

from utils import *

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SERVER_IP, SERVER_PORT))

print('Welcome to Secure Internet Poker')

while True:
    data, data_type = recv_msg(client_socket)

    if data_type == MessageType.CARDS.value:
        cards = data[1:-1].split(', ')
        print('Your cards are ', data)
    elif data_type == MessageType.TURN.value:
        num = -1

        while True:
            num = input('Pick a card: ')
            if num in cards:
                packet = create_packet(num, MessageType.CHOICE)
                client_socket.send(packet)
                break
    elif data_type == MessageType.WIN.value:
        print('Result: WIN')
    elif data_type == MessageType.LOSE.value:
        print('Result: LOSE')
    elif data_type == MessageType.TIE.value:
        print('Result: TIE')
    elif data_type == MessageType.END.value:
        print('Thanks for playing!')
        client_socket.close()
        input('Press any key to continue')
        exit()