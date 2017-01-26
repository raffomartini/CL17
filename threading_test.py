from threading import Thread, Lock
import time, random

output_print_lock = Lock()
threads = []

def threading_test(var):
    '''
    Print the variable
    :param var:
    :return: Nothing
    '''
    time.sleep(random.randrange(10)*0.1)
    output_print_lock.acquire()
    print('This is thread number {}'.format(var))
    output_print_lock.release()
    time.sleep(random.randrange(5))
    output_print_lock.acquire()
    print('Thread {} done'.format(var))
    output_print_lock.release()

for num in range(5):
    worker = Thread(target=threading_test, args=(num,))
    threads.append(worker)
    worker.setDaemon(True)
    worker.start()

for thread in threads:
    thread.join()
print('Done')
