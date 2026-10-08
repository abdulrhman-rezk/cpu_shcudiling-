# generate fake processes data to train on
# 0 = cpu bound .. long burst and low io
# 1 = io bound .. short burst and high io

import numpy as np
import pandas as pd


def generate_processes(n) :
    np.random.seed(42)   # same data every run

    burst_time = np.random.randint(5, 200, size=n)       # ms
    io_frequency = np.random.randint(0, 20, size=n)      # number of io requests
    memory_usage = np.random.randint(50, 2048, size=n)   # MB

    # the labels
    labels = []
    for i in range(n) :
        if burst_time[i] >= 100 and io_frequency[i] <= 5 :
            labels.append(0)
        elif burst_time[i] <= 50 and io_frequency[i] >= 10 :
            labels.append(1)
        else :
            # mixed .. the stronger side win
            if burst_time[i] > io_frequency[i] * 5 :
                labels.append(0)
            else :
                labels.append(1)

    data = {
        'burst_time': burst_time,
        'io_frequency': io_frequency,
        'memory_usage': memory_usage,
        'process_type': labels
    }

    return pd.DataFrame(data)


# end point
df = generate_processes(10000)
df.to_csv('processes_data.csv', index=False)
print(f'saved {len(df)} rows -> processes_data.csv')
print(df['process_type'].value_counts().rename({0 : 'cpu bound', 1 : 'io bound'}))
