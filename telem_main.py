from multiprocessing import Process, Queue
from main_telem import telem_tools
import time
import numpy as np


GLOBAL_WINDOW_SIZE = 1000

def data_read_daemon(queue, ringbuf):
    """
    Data reading process (psuedo-daemon)
    Fills up window data, then triggers
    window analysis process
    """
    window_counter = GLOBAL_WINDOW_SIZE
    data_counter = 0
    print("Started Sensor Read Daemon")

    while True:
        # Expect some of the communications to be VERY slow
        time.sleep(np.random.random()*0.01)
        data = np.random.randint(0, 100) # Random data (temporary)

        # print(data)
        ringbuf.extend(np.array([data])) # place data in the ring buffer

        window_counter -= 1 # Decrement local window size counter
        if window_counter == 0:
            # Process the data currently in the ring buffer
            ring_data = ringbuf.get()
            data_counter += 1
            print("Buffer filled")
            # print(ring_data)
            window_counter = GLOBAL_WINDOW_SIZE
            # Send off to window process function
            pw = Process(target=process_window_data,
                         args=(ring_data, data_counter, queue))
            pw.start()


def process_window_data(data, data_count, queue):
    """
    Process for saving the windowed timeseries data
    for analysis via metrics or streaming algorithms.
    Places data on queue for long-term storage
    """
    time.sleep(3) # Simulating data send delay (temporary)
    print("large data read, saving...", data_count)
    queue.put(data) # placing read data in the queue


def store_window_data(queue):
    """
    Process for Saving the data in long-term storage
    """
    while True:
        if queue.empty() is True:
            pass # nothing to do
        else:
            if queue.full() is True:
                print("WARNING: QUEUE IS FULL")
            print("taking off queue")
            data = queue.get()
            time.sleep(5) # Simulating data send delay (temporary)
            print("Long term storage done")

if __name__ == '__main__':
    """
    Main Loop of the telemetry system

    Operated by a multiprocessing queue which reads/stores data
    and uses a ring buffer in NumPy to create a window/snapshot
    of time series data to process in algorithms or streaming
    machine learning algorithms.
    """
    # Main shared Queue and Ring Buffer
    q = Queue()
    ringbuf = telem_tools.RingBuffer(GLOBAL_WINDOW_SIZE)

    # Start data read daemon
    dr = Process(target=data_read_daemon, args=(q,ringbuf))
    dr.start()

    # Start write daemon
    wr = Process(target=store_window_data, args=(q,))
    wr.start()

    while True:
        time.sleep(0.1)
        # This is the place where your main loop or logic goes
