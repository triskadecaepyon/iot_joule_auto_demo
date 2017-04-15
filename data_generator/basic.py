import time
import numpy as np

"""
A basic stub script to generate random data every second in
a list format.
"""


def data_inf(obj):
    """
    A method to make infinite data streams via a generator.
    """
    while True:
        data = [np.random.ranf(), np.random.ranf(), np.random.ranf(),
                np.random.ranf(), np.random.ranf(), np.random.ranf()]
        time.sleep(0.5)
        yield data


def sensor_data_read():
    """
    A stubbed method that simulates sensor read times,
    and randomly generated data.
    """
    basic_gen = data_inf(1)
    next(basic_gen)
    return basic_gen.send(1)


if __name__ == "__main__":
    basic_gen = data_inf(1)
    next(basic_gen) # initialize the generator
    while True:
        print(basic_gen.send(1))
