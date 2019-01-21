import thread


def print_num(num):
    print num


for i in range(5):
    thread.start_new_thread(print_num, tuple([i]))