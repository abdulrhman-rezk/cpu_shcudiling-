# smart cpu scheduler
# compare the normal round robin (same quantum for all) with the ai round robin
# the model decide every process cpu bound or io bound .. and give him the right quantum

import numpy as np
import matplotlib.pyplot as plt

from processes import generate_processes
from scheduler import traditional_rr, ai_rr


# help function
def read_number(msg) :
    try :
        return int(input(msg))
    except ValueError :
        return -1


def show_processes(processes) :
    print('what the model decided')
    print('-' * 70)
    print('PID\tBurst\tIO\tMemory\tType\t\tQuantum')
    print('-' * 70)
    for p in processes :
        ptype = 'io bound' if p.process_type == 1 else 'cpu bound'
        print(f'{p.pid}\t{p.burst_time}ms\t{p.io_frequency}\t{p.memory_usage}MB\t{ptype}\t\t{p.quantum}ms')
    print('-' * 70)


def show_results(processes) :
    print('scheduling comparison')
    print('-' * 70)
    print('PID\tBurst\tstd RR WT\tAI RR WT\tsaved')
    print('-' * 70)
    for p in processes :
        saved = p.waiting_std - p.waiting_ai
        print(f'{p.pid}\t{p.burst_time}ms\t{p.waiting_std}ms\t\t{p.waiting_ai}ms\t\t{saved}ms')
    print('-' * 70)


def show_charts(processes) :
    avg_std = sum(p.waiting_std for p in processes) / len(processes)
    avg_ai = sum(p.waiting_ai for p in processes) / len(processes)

    # chart 1 .. average waiting time
    plt.bar(['Standard RR', 'AI RR'], [avg_std, avg_ai], color=['red', 'green'])
    plt.title('Average Waiting Time')
    plt.ylabel('ms')
    plt.show()

    # chart 2 .. first 10 processes
    first10 = processes[:10]
    pids = [p.pid for p in first10]
    x = np.arange(len(pids))
    width = 0.35

    plt.bar(x - width/2, [p.waiting_std for p in first10], width, label='Standard RR')
    plt.bar(x + width/2, [p.waiting_ai for p in first10], width, label='AI RR')
    plt.xticks(x, pids)
    plt.title('Waiting Time (first 10 processes)')
    plt.ylabel('ms')
    plt.legend()
    plt.show()


# heart of app
def main() :
    print('smart cpu scheduler')
    print('-' * 30)

    n = 0
    while n <= 0 :
        n = read_number('how many processes to simulate : ')
        if n <= 0 :
            print('enter a positive number!')

    processes = generate_processes(n)

    # the model read every process and choose the quantum
    ai_rr(processes)
    show_processes(processes)

    # run the two schedulers and compare
    traditional_rr(processes)

    print()
    show_results(processes)

    avg_std = sum(p.waiting_std for p in processes) / len(processes)
    avg_ai = sum(p.waiting_ai for p in processes) / len(processes)
    print(f'standard RR avg waiting : {avg_std:.1f} ms')
    print(f'ai RR avg waiting       : {avg_ai:.1f} ms')

    if avg_ai < avg_std :
        print(f'\nthe ai scheduler saved {100 - (avg_ai / avg_std * 100):.1f} % of the waiting time!')
    else :
        print('\nthis time the standard RR was better .. try again')

    input('\npress enter to see the charts...')
    show_charts(processes)
    print('bye!')


# end point
main()
