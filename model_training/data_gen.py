
import numpy as np
import pandas as pd


def generate_processes(n=10000):
    """Generate n synthetic processes with burst_time, io_frequency, memory_usage, and process_type label."""
    np.random.seed(42)

    burst_time    = np.random.randint(5, 200, size=n)       # ms
    io_frequency  = np.random.randint(0, 20, size=n)        # number of IO requests
    memory_usage  = np.random.randint(50, 2048, size=n)     # MB

    # Labeling logic:
    #   CPU-bound  (0): high burst, low IO
    #   I/O-bound  (1): low burst, high IO
    labels = []
    for i in range(n):
        if burst_time[i] >= 100 and io_frequency[i] <= 5:
            labels.append(0)   # CPU-bound
        elif burst_time[i] <= 50 and io_frequency[i] >= 10:
            labels.append(1)   # I/O-bound
        else:
            # Mixed — assign based on dominant characteristic
            if burst_time[i] > io_frequency[i] * 5:
                labels.append(0)
            else:
                labels.append(1)

    data = {
        "burst_time":    burst_time,
        "io_frequency":  io_frequency,
        "memory_usage":  memory_usage,
        "process_type":  labels,
    }

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_processes(500000)
    df.to_csv("processes_data.csv", index=False)
    print(f"[OK] Dataset saved -> processes_data.csv  ({len(df)} rows)")
    print(df["process_type"].value_counts().rename({0: "CPU-bound", 1: "I/O-bound"}).to_string())
