import socket
import time
import struct
import random


HOST = "127.0.0.1"
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
    sc.connect((HOST, PORT))

    local_time = time.time() + random.uniform(-5, 5)
    print(f" Client local time before adjustment: {local_time}")

    request = sc.recv(1024)
    
    if request == b'TIME_REQUEST':
        sc.send(struct.pack('f', local_time))

    adjustment = struct.unpack('f', sc.recv(4))[0]
    print(f"Adjustment received from server {adjustment}")

    new_time = local_time + adjustment
    print(f"Server new time {new_time}")

    sc.close()
