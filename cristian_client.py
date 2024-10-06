############################# 
# Cristian Client using 
# sockets
# Author: Duran Macedo Elliot
# Date: 24-09-2024
# #############################


import socket
import time
import datetime


def str_to_datetime(x: str) -> datetime:
    return datetime.datetime.strptime(x, '%Y%m%d%H:%M:%f')


HOST = "192.168.132.128"
PORT = 9099


sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

t0 = time.time()
sc.connect((HOST, PORT))
server_time = sc.recv(4096).decode()
t1 = time.time()

Cs: datetime = str_to_datetime(server_time)
Cc: datetime = datetime.datetime.now()
c = Cs + datetime.timedelta(seconds=(t1-t0)/2)

print("Server time", Cs)
print("Client time before adjustment", Cc)
print("Exact time is", Cs+datetime.timedelta(seconds=t1-t0))

if c < Cc:
    aux = Cc-c
    time.sleep(aux.total_seconds() / (24 * 3600))
    Cc = datetime.datetime.now()
else:
    Cc = c

print("Client time after adjustment", Cc)

sc.close()
