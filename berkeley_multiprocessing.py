############################# 
# Berkeley Algorithm using 
# multiprocessing
# Author: Duran Macedo Elliot
# Date: 03-10-2024
#############################


from multiprocessing import Process, Pipe
import time
import random


MESSAGE = "TIME_REQUEST"


def server_process(server):
    server.send(MESSAGE)
    client_time = server.recv()
    print(f"Time received from client: {client_time}")

    server_time = time.time()
    print(f"Server time (Master): {server_time}")

    adjustment = server_time - client_time
    print(f"Send adjustment {adjustment} to client")
    server.send(adjustment)


def client_process(client):
    local_time = time.time() + random.uniform(-5, 5)
    print(f"Client local time before adjustment: {local_time}")

    request = client.recv()

    if request == MESSAGE:
        client.send(local_time)

    adjustment = client.recv()
    print(f"Adjustment received from server {adjustment}")

    new_time = local_time + adjustment
    print(f"Server new time {new_time}")


if __name__ == '__main__':
    server, client = Pipe()

    process1 = Process(target=server_process,
                       args=(server,))

    process2 = Process(target=client_process,
                       args=(client,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()
