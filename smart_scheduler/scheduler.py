# the scheduling logic
# the model say every process cpu bound or io bound .. and the type choose the quantum

import joblib
import os
import warnings

# hide the sklearn warning when i predict with a normal list
warnings.filterwarnings('ignore', message='X does not have valid feature names')

_model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'model_training', 'scheduler_model.pkl'))

FIXED_QUANTUM = 5      # the normal round robin
CPU_BOUND_QUANTUM = 5  # small .. so the long process dont hog the cpu
IO_BOUND_QUANTUM = 20  # big .. so the short io process finish fast


# help function .. round robin but every process have his own quantum
def simulate_rr(processes, quantum_map) :
    remaining = {p.pid : p.burst_time for p in processes}
    order = [p.pid for p in processes]
    finish_time = {}
    t = 0   # all arrive at time 0

    while any(remaining[pid] > 0 for pid in order) :
        for pid in order :
            if remaining[pid] <= 0 :
                continue
            executed = min(remaining[pid], quantum_map[pid])
            remaining[pid] -= executed
            t += executed
            if remaining[pid] == 0 :
                finish_time[pid] = t

    waiting = []
    for p in processes :
        waiting.append(finish_time[p.pid] - p.burst_time)

    return waiting


def predict_process_type(p) :
    features = [[p.burst_time, p.io_frequency, p.memory_usage]]
    return int(_model.predict(features)[0])


def traditional_rr(processes) :
    quantum_map = {p.pid : FIXED_QUANTUM for p in processes}
    waiting = simulate_rr(processes, quantum_map)

    for i in range(len(processes)) :
        processes[i].waiting_std = waiting[i]


def ai_rr(processes) :
    # the model decide the type .. and the type decide the quantum
    for p in processes :
        p.process_type = predict_process_type(p)
        p.quantum = IO_BOUND_QUANTUM if p.process_type == 1 else CPU_BOUND_QUANTUM

    quantum_map = {p.pid : p.quantum for p in processes}
    waiting = simulate_rr(processes, quantum_map)

    for i in range(len(processes)) :
        processes[i].waiting_ai = waiting[i]
