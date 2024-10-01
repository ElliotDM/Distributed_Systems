from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def local_time(counter):
    return '(LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1


def event(pid, counter):
    counter += 1
    print('Something happen in {} !'.
          format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message sended to' + str(pid) + local_time(counter))
    return counter


def process_one(pipe12):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)


def process_two(pipe21, pipe23):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)


def process_three(pipe32, pipe34):
    pid = getpid()
    counter = 0
    counter = send_message(pipe34, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = recv_message(pipe34, pid, counter)
    counter = send_message(pipe34, pid, counter)


def process_four(pipe43, pipe45):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe43, pid, counter)
    counter = send_message(pipe45, pid, counter)
    counter = recv_message(pipe45, pid, counter)
    counter = send_message(pipe43, pid, counter)
    counter = recv_message(pipe43, pid, counter)


def process_five(pipe54, pipe56):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe54, pid, counter)
    counter = send_message(pipe54, pid, counter)
    counter = send_message(pipe56, pid, counter)
    counter = recv_message(pipe56, pid, counter)


def process_six(pipe65):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe65, pid, counter)
    counter = send_message(pipe65, pid, counter)


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
