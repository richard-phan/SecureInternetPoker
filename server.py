import socket
import select

from utils import *

def close_connections(socket_list):
    for conn in socket_list:
        conn.send(packetClose)

def send_outcomes(socket_list, cards):
    packetWin = create_packet('', MessageType.WIN)
    packetLose = create_packet('', MessageType.LOSE)

    if cards[0] > cards[1]:
        socket_list[0].send(packetWin)
        socket_list[1].send(packetLose)
    elif cards[1] > cards[0]:
        socket_list[1].send(packetWin)
        socket_list[0].send(packetLose)
    else:
        packetTie = create_packet('', MessageType.TIE)
        socket_list[0].send(packetTie)
        socket_list[1].send(packetTie)
                

PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('', PORT))
server_socket.listen(2)

while True:
    socket_list = []

    while len(socket_list) < 2:
        print('Waiting for connections...')

        main_socket, addr = server_socket.accept()
        socket_list.append(main_socket)

        print('{}:{} has connected'.format(addr[0], addr[1]))

    for round in range(3):
        for connection in socket_list:
            nums = generate_numbers(1, 15, 3)
            packet = create_packet(nums, MessageType.CARDS)
            connection.send(packet)

        cards = []
        for conn in range(len(socket_list)):
            packet = create_packet('', MessageType.TURN)
            socket_list[conn].send(packet)

            data, data_type = recv_msg(socket_list[conn])
            cards.append(data)


    packetClose = create_packet('', MessageType.END)
    close_connections(socket_list)