from multiprocessing import Process, Queue
import time
import numpy as np


GLOBAL_WINDOW_SIZE = 100


def store_data(queue):
    """
    Storage process, used to take data off the queue from
    sensor reads and store it to short term HDF5.
    """
    time.sleep(0.25) # Simulating data delay (temporary)
    data = queue.get()
    # print('Saving', data)


def process_window_data(data, data_count):
    """
    Process for saving the windowed timeseries data
    for analysis via metrics or streaming algorithms
    Not meant for HDF5, but for feeding NumPy arrays
    to other functions or processes.
    """
    time.sleep(5) # Simulating data send delay (temporary)
    print("large data read, saving...", data_count)


class RingBuffer():
    """
    https://scimusing.wordpress.com/2013/10/25/ring-buffers-in-pythonnumpy/
    TODO: migrate to the RingBuffer package at:
    https://github.com/eric-wieser/numpy_ringbuffer
    """
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.zeros(length, dtype='f')
        self.index = 0

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) %self.data.size
        return self.data[idx]


if __name__ == '__main__':
    """
    Main Loop of the telemetry system

    Operated by a multiprocessing queue which reads/stores data
    and uses a ring buffer in NumPy to create a window/snapshot
    of time series data to process in algorithms or streaming
    machine learning algorithms.
    """
    q = Queue()
    ringbuf = RingBuffer(GLOBAL_WINDOW_SIZE)
    window_counter = GLOBAL_WINDOW_SIZE
    data_counter = 0

    while True:
        # time.sleep(0.1)
        # This is the data read process; simulating when data is ready
        if (np.random.randint(0,2)):
            data = np.random.randint(0, 100) # Random data (temporary)
            # print(data)
            q.put(data) # placing read data in the queue
            ringbuf.extend(np.array([data])) # place data in the ring buffer

            window_counter -= 1 # Decrement local window size counter
            if window_counter == 0:
                # Process the data currently in the ring buffer
                ring_data = ringbuf.get()
                data_counter += 1
                print(ring_data)
                window_counter = GLOBAL_WINDOW_SIZE
                # Send off to window process function
                pw = Process(target=process_window_data,
                             args=(ring_data, data_counter))
                pw.start()

            # Longer storage process to HDF5
            s = Process(target=store_data, args=(q,))
            s.start() # Don't need join, non-blocking for better response

        else:
            pass
            # print("Waiting")
            # We don't use join as to not block the calculation
