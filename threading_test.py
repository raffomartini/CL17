from threading import Thread, Lock
import time, random

output_print_lock = Lock()
threads = []

def syncronize(lock):
    '''
    Decorator to syncronize methonds / functions
    :param lock: a lock, obtained from threading.Lock()
    :return:
    '''

    def wrap(f):
        def newFunction(*args, **kwargs):
            lock.acquire()
            try:
                return f(*args, **kwargs)
            finally:
                lock.release()
        return newFunction
    return wrap

def threading_test(var):
    '''
    Print the variable
    :param var:
    :return: Nothing
    '''
    time.sleep(random.randrange(10)*0.1)

    # @synchronized(myLock)
    output_print_lock.acquire()
    print('This is thread number {}'.format(var))
    output_print_lock.release()
    time.sleep(random.randrange(5))
    output_print_lock.acquire()
    print('Thread {} done'.format(var))
    output_print_lock.release()


for num in range(2):
    worker = Thread(target=threading_test, args=(num,))
    threads.append(worker)
    worker.setDaemon(True)
    worker.start()




for thread in threads:
    thread.join()
print('Done')
