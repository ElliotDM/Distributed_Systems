from multiprocessing import Process, Pipe
import datetime
import time


def str_to_datetime(x: str) -> datetime:
    return datetime.datetime.strptime(x, '%Y%m%d%H:%M:%f')


def server_conn(conn):
    msg = conn.recv()
    date = datetime.datetime.now()  # Cs
    date_str = date.strftime('%Y%m%d%H:%M:%f')

    conn.send(date_str)


if __name__ == '__main__':
    server, client = Pipe()

    process = Process(target=server_conn,
                      args=(server,))

    process.start()

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

    process.join()
