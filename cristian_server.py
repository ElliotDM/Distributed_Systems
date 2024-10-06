############################# 
# Cristian Server using 
# sockets
# Author: Duran Macedo Elliot
# Date: 24-09-2024
# #############################


import socket
import datetime

HOST = "192.168.132.128"
PORT = 9099
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((HOST, PORT))
ss.listen()

while True:
    conn, addr = ss.accept()
    print("Connecting with client ", addr)

    date = datetime.datetime.now() # Cs
    date_str = date.strftime('%Y%m%d%H:%M:%f')

    print("Sending time to ", addr)
    print(date)
    
    conn.send(date_str.encode())
    conn.close()
