############################# 
# Berkeley Server using 
# sockets
# Author: Duran Macedo Elliot
# Date: 27-09-2024
# #############################


import socket
import time
import struct

HOST = "192.168.132.128"
PORT = 12345
num_clients = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.bind((HOST, PORT))
    ss.listen(num_clients)
    print("Waiting for clients...")

    connections = []
    times = []
    
    for _ in range(num_clients):
        conn, addr = ss.accept()
        print(f"Connection establish with {addr}")
        connections.append(conn)

    for conn in connections:    
        conn.send(b'TIME_REQUEST')

    for conn in connections:
        client_time = struct.unpack('f', conn.recv(4))[0]
        print(f"Time received from client: {client_time}")
        times.append(client_time)

    server_time = time.time()
    print(f"Server time (Master): {server_time}")

    adjustments = [server_time - client_time for client_time in times]

    for conn, adjustment in zip(connections, adjustments):
        print(f"Send adjustment {adjustment} to client")
        conn.send(struct.pack('f', adjustment))

    for conn in connections:
        conn.close()
