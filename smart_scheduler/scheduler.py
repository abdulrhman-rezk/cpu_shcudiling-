
import joblib
import os
import warnings

# Suppress sklearn's feature-name warning when predicting with plain lists.
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# Load model once at import time.
_model_path = os.path.join(os.path.dirname(__file__), "scheduler_model.pkl")
_model = joblib.load(_model_path)

# Quanta (ms)
FIXED_QUANTUM     = 5    # Standard RR baseline
CPU_BOUND_QUANTUM = 5    # Small: prevents CPU-heavy processes from hogging
IO_BOUND_QUANTUM  = 20   # Large: short I/O processes finish in one round


def _simulate_rr(processes, quantum_map):
    remaining    = {p["pid"]: p["burst_time"] for p in processes}
    order        = [p["pid"] for p in processes]
    finish_time  = {}
    arrival_time = {p["pid"]: 0 for p in processes}
    t = 0

    while any(remaining[pid] > 0 for pid in order):
        made_progress = False
        for pid in order:
            if remaining[pid] <= 0:
                continue
            executed       = min(remaining[pid], quantum_map[pid])
            remaining[pid] -= executed
            t              += executed
            made_progress   = True
            if remaining[pid] == 0:
                finish_time[pid] = t
        if not made_progress:
            break

    results = []
    for p in processes:
        pid        = p["pid"]
        turnaround = finish_time.get(pid, t) - arrival_time[pid]
        results.append({"pid": pid, "waiting_time": max(0, turnaround - p["burst_time"])})
    return results


def traditional_round_robin(processes):
    quantum_map = {p["pid"]: FIXED_QUANTUM for p in processes}
    return _simulate_rr(processes, quantum_map)


def predict_process_type(process):
    features = [[process["burst_time"], process["io_frequency"], process["memory_usage"]]]
    return int(_model.predict(features)[0])


def ai_round_robin(processes):

    quantum_map  = {}
    predictions  = {}

    for p in processes:
        ptype                = predict_process_type(p)
        predictions[p["pid"]] = ptype
        quantum_map[p["pid"]] = IO_BOUND_QUANTUM if ptype == 1 else CPU_BOUND_QUANTUM

    rr_results = _simulate_rr(processes, quantum_map)

    return [
        {
            "pid":            r["pid"],
            "predicted_type": predictions[r["pid"]],
            "quantum":        quantum_map[r["pid"]],
            "waiting_time":   r["waiting_time"],
        }
        for r in rr_results
    ]
