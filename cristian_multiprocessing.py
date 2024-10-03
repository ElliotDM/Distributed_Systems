from multiprocessing import Process, Pipe
import datetime
import time


def str_to_datetime(x: str) -> datetime:
    return datetime.datetime.strptime(x, '%Y%m%d%H:%M:%f')


def server_process(server):
    msg = server.recv()
    date = datetime.datetime.now()  # Cs
    date_str = date.strftime('%Y%m%d%H:%M:%f')

    server.send(date_str)


def client_process(client):
    t0 = time.time()
    client.send("Message")
    server_time = client.recv()
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
