from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def local_time(vector):
    return '(VECTOR_TIME={}, LOCAL_TIME={})'.format(vector, datetime.now())


def calc_recv_timestamp(recv_time_stamp, vector):
    return [max(vc1, vc2) for vc1, vc2 in zip(recv_time_stamp, vector)]


def event(pid, vector, idx):
    vector[idx] += 1
    print('Something happen in {} !'.
          format(pid) + local_time(vector))
    return vector


def send_message(pipe, pid, vector, idx):
    vector[idx] += 1
    pipe.send(('Empty shell', vector))
    print('Message sent from ' + str(pid) + local_time(vector))
    return vector


def recv_message(pipe, pid, vector, idx):
    message, timestamp = pipe.recv()
    vector = calc_recv_timestamp(timestamp, vector)
    vector[idx] += 1
    print('Message sended to ' + str(pid) + local_time(vector))
    return vector


def process_one(pipe12):
    pid = getpid()
    vector = [0]*6
    idx = 0
    vector = event(pid, vector, idx)
    vector = send_message(pipe12, pid, vector, idx)
    vector = event(pid, vector, idx)
    vector = recv_message(pipe12, pid, vector, idx)
    vector = send_message(pipe12, pid, vector, idx)


def process_two(pipe21, pipe23):
    pid = getpid()
    vector = [0]*6
    idx = 1
    vector = recv_message(pipe21, pid, vector, idx)
    vector = send_message(pipe23, pid, vector, idx)
    vector = send_message(pipe21, pid, vector, idx)
    vector = recv_message(pipe21, pid, vector, idx)


def process_three(pipe32, pipe34):
    pid = getpid()
    vector = [0]*6
    idx = 2
    vector = send_message(pipe34, pid, vector, idx)
    vector = event(pid, vector, idx)
    vector = recv_message(pipe32, pid, vector, idx)
    vector = recv_message(pipe34, pid, vector, idx)
    vector = send_message(pipe34, pid, vector, idx)


def process_four(pipe43, pipe45):
    pid = getpid()
    vector = [0]*6
    idx = 3
    vector = recv_message(pipe43, pid, vector, idx)
    vector = send_message(pipe45, pid, vector, idx)
    vector = recv_message(pipe45, pid, vector, idx)
    vector = send_message(pipe43, pid, vector, idx)
    vector = recv_message(pipe43, pid, vector, idx)


def process_five(pipe54, pipe56):
    pid = getpid()
    vector = [0]*6
    idx = 4
    vector = recv_message(pipe54, pid, vector, idx)
    vector = send_message(pipe54, pid, vector, idx)
    vector = send_message(pipe56, pid, vector, idx)
    vector = recv_message(pipe56, pid, vector, idx)


def process_six(pipe65):
    pid = getpid()
    vector = [0]*6
    idx = 5
    vector = recv_message(pipe65, pid, vector, idx)
    vector = send_message(pipe65, pid, vector, idx)


if __name__ == '__main__':
    one_two, two_one = Pipe()
    two_three, three_two = Pipe()
    three_four, four_three = Pipe()
    four_five, five_four = Pipe()
    five_six, six_five = Pipe()

    process1 = Process(target=process_one,
                       args=(one_two,))

    process2 = Process(target=process_two,
                       args=(two_one, two_three))
    
    process3 = Process(target=process_three,
                       args=(three_two, three_four))
    
    process4 = Process(target=process_four,
                       args=(four_three, four_five))
    
    process5 = Process(target=process_five,
                       args=(five_four, five_six))
    
    process6 = Process(target=process_six,
                       args=(six_five,))

    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    process6.join()
