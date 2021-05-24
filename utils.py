import socket
import random

from enum import Enum

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

def create_packet(data, data_type):
    data_len = str(len(data))
    padding = len(data_len)
    return ('0' * (HEADER_LENGTH - padding - 1) + data_len + data_type.value + data).encode('utf-8')

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