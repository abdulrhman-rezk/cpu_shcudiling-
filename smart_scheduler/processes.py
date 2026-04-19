import random

def generate_simulation_processes(n):
    processes = []
    for i in range(1, n + 1):
        process = {
            "pid":           f"P{i}",
            "burst_time":    random.randint(5, 150),    # ms
            "io_frequency":  random.randint(0, 18),     # number of IO requests
            "memory_usage":  random.randint(64, 1024),  # MB
        }
        processes.append(process)
    return processes
