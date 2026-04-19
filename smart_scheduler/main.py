import sys
import time
import os
import itertools
import matplotlib.pyplot as plt
import numpy as np

from processes import generate_simulation_processes
from scheduler import traditional_round_robin, ai_round_robin

def show_loading_spinner(message, seconds):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + seconds
    spinner = itertools.cycle(frames)
    
    while time.time() < end_time:
        sys.stdout.write(f"\r  {next(spinner)}  {message}  ")
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write(f"\r  ✔  {message}  Done!   \n")

def show_charts(processes, rr_results, ai_results, avg_rr, avg_ai):
    plt.style.use('ggplot')
    
    # 1. رسمة لمتوسط وقت الانتظار
    plt.figure(figsize=(6, 4))
    bars = plt.bar(["Standard RR", "AI Scheduler"], [avg_rr, avg_ai], color=['#e24a33', '#348abd'])
    plt.title("Average Waiting Time Comparison")
    plt.ylabel("Waiting Time (ms)")
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f"{yval:.1f} ms", va='bottom', ha='center', fontweight='bold')
        
    plt.show()

    # 2. رسمة لأول 10 عمليات عشان نقارن بينهم ببساطة
    num_to_show = min(10, len(processes))
    pids = [p["pid"] for p in processes[:num_to_show]]
    rr_vals = [r["waiting_time"] for r in rr_results[:num_to_show]]
    ai_vals = [r["waiting_time"] for r in ai_results[:num_to_show]]
    
    x = np.arange(len(pids))
    width = 0.35

    plt.figure(figsize=(10, 5))
    bars1 = plt.bar(x - width/2, rr_vals, width, label='Standard RR', color='#e24a33')
    bars2 = plt.bar(x + width/2, ai_vals, width, label='AI Scheduler', color='#348abd')
    plt.xticks(x, pids)
    plt.title("Per-Process Waiting Time (First 10 processes)")
    plt.ylabel("Waiting Time (ms)")
    plt.legend()
    
    # وضع الأرقام فوق الأعمدة
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f"{int(yval)}", va='bottom', ha='center', fontsize=8)
    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f"{int(yval)}", va='bottom', ha='center', fontsize=8)

    plt.show()

def main():
    print("AI-Driven CPU Scheduling Simulator")
    print("----------------------------------\n")

    while True:
        try:
            n = int(input("Enter the number of processes to simulate: "))
            if n > 0:
                break
            print("Please enter a positive number.\n")
        except ValueError:
            print("Invalid input. Please enter an integer.\n")

    print()
    show_loading_spinner("Generating processes...", 1.5)
    processes = generate_simulation_processes(n)

    ai_results = ai_round_robin(processes)
    
    print("\nAI Process Analysis")
    print("-------------------")
    for p in processes:
        pid = p["pid"]

        r = next(item for item in ai_results if item["pid"] == pid)
        
        io_level = "Low" if p["io_frequency"] <= 5 else ("High" if p["io_frequency"] >= 10 else "Med")
        ptype = "CPU-BOUND" if r["predicted_type"] == 0 else "I/O-BOUND"
        
        print(f"[{pid}]\tBurst: {p['burst_time']}ms \tIO: {io_level} \t-> {ptype} \t-> Quantum: {r['quantum']}ms")
        time.sleep(0.05)

    print()
    show_loading_spinner("Running Scheduling Algorithms...", 2)
    rr_results = traditional_round_robin(processes)

    print("\nScheduling Comparison")
    print("---------------------")

    print("PID\tBurst\tStd RR WT\tAI Quantum\tAI WT\tSaved")
    print("-" * 75)

    rr_by_pid = {r["pid"]: r["waiting_time"] for r in rr_results}
    ai_by_pid = {r["pid"]: r for r in ai_results}

    for p in processes:
        pid = p["pid"]
        burst = p["burst_time"]
        rr_wt = rr_by_pid[pid]
        ai_wt = ai_by_pid[pid]["waiting_time"]
        ai_q = ai_by_pid[pid]["quantum"]
        saved = rr_wt - ai_wt
        
        print(f"{pid}\t{burst}ms\t{rr_wt}ms\t\t{ai_q}ms\t\t{ai_wt}ms\t{saved}ms")
        time.sleep(0.05)

    print("-" * 75)

    avg_rr = sum(r["waiting_time"] for r in rr_results) / len(rr_results)
    avg_ai = sum(r["waiting_time"] for r in ai_results) / len(ai_results)
    pct = ((avg_rr - avg_ai) / avg_rr * 100) if avg_rr > 0 else 0.0

    print("\nSummary")
    print("-------")
    print(f"Standard RR  Avg Waiting Time : {avg_rr:.1f} ms")
    print(f"AI Scheduler Avg Waiting Time : {avg_ai:.1f} ms")
    
    if pct >= 0:
        print(f"\nAI Scheduler is {pct:.1f}% faster on average.\n")
    else:
        print(f"\nAI Scheduler is {abs(pct):.1f}% slower on average.\n")

    input("Press Enter to view the charts...")
    show_charts(processes, rr_results, ai_results, avg_rr, avg_ai)

if __name__ == "__main__":
    main()
