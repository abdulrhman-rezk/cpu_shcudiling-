# process class .. the thing the scheduler work on

import random


class Process :
    def __init__(self, pid, burst_time, io_frequency, memory_usage):
        self.pid = pid
        self.burst_time = burst_time
        self.io_frequency = io_frequency
        self.memory_usage = memory_usage

        # the model and the scheduler will fill those later
        self.process_type = None
        self.quantum = None
        self.waiting_std = None
        self.waiting_ai = None


# help function
def generate_processes(n) :
    processes = []
    for i in range(1, n + 1) :
        p = Process(
            f'P{i}',
            random.randint(5, 150),     # ms
            random.randint(0, 18),      # number of io requests
            random.randint(64, 1024)    # MB
        )
        processes.append(p)

    return processes
