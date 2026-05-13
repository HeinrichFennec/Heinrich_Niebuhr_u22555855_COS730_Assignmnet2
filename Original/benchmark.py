"""
This is my benchmark script for Task 6. I run it from inside either
my Task 1 (baseline) or Task 5 (optimised) source directory and it
prints everything I needed for the comparison: method calls per
scenario, execution time per scenario, and the radon metrics
(cyclomatic complexity and maintainability index) for each file.

I noticed that every class in my system already prints a trace line
of the form "[ClassName] methodName" whenever one of its methods runs.
So instead of building anything fancy, I just capture stdout for one
run of each scenario and count how many lines start with "[". That's
my method-call count.

For execution time I silence stdout so the prints don't slow the loop
down, warm up for a bit so the timer settles, then run each scenario
10000 times with time.perf_counter() and report the mean in microseconds.

For the complexity and maintainability index I just shell out to radon,
which I installed with `pip install radon`. I invoke it as a Python
module (python -m radon) so it works the same on Windows as on Linux.

Run with: python benchmark.py
"""
import io
import os
import subprocess
import sys
import time
from contextlib import redirect_stdout

# VS Code runs the script from the workspace folder instead of the script's folder, which breaks os.listdir(".") for me. So I cd to wherever this script actually lives before doing anything else.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import main


def count_calls(scenario):
    # I capture stdout into a buffer so I can read back exactly what was printed during this scenario, then count the trace lines.
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        scenario()
    lines = buffer.getvalue().splitlines()
    return sum(1 for line in lines if line.startswith("["))


def time_runs(scenario, runs=10000, warmup=500):
    # I redirect stdout to /dev/null so my trace prints don't dominate what I'm trying to measure. I do this once before the loop so I'm not paying for the context manager on every iteration.
    null = open(os.devnull, "w")
    saved_stdout = sys.stdout
    sys.stdout = null
    try:
        # I run a few hundred warm-up iterations first because the very first calls are usually slower (imports, caching, etc.) and I don't want those skewing my average.
        for _ in range(warmup):
            scenario()
        start = time.perf_counter()
        for _ in range(runs):
            scenario()
        elapsed = time.perf_counter() - start
    finally:
        sys.stdout = saved_stdout
        null.close()
    return (elapsed / runs) * 1_000_000


def run_radon(metric):
    # I only want the metrics for the system code, so I exclude main.py(which is just my test harness) and this benchmark file itself.
    files = sorted(f for f in os.listdir(".") if f.endswith(".py")
                   and f not in ("main.py", "benchmark.py"))
    # I invoke radon via python -m so it uses the same Python that's running this script (sys.executable). That way I know it'll find radon I installed with pip.
    cmd = [sys.executable, "-m", "radon", metric, "-s"]
    if metric == "cc":
        cmd.append("-a")  # show the average complexity at the end
    cmd.extend(files)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


scenarios = [
    ("invalid",  main.run_invalid),
    ("accept",   main.run_accept),
    ("reject",   main.run_reject),
    ("revision", main.run_revision),
]


print("=" * 50)
print("Method calls and execution time per scenario")
print("=" * 50)
print(f"{'scenario':10s} | {'calls':>5s} | {'mean us':>9s}")
print("-" * 32)
total_calls = 0
for name, func in scenarios:
    calls = count_calls(func)
    mean_us = time_runs(func)
    total_calls += calls
    print(f"{name:10s} | {calls:5d} | {mean_us:9.2f}")
print(f"{'total':10s} | {total_calls:5d} |")

print()
print("=" * 50)
print("Cyclomatic complexity per method (radon cc)")
print("=" * 50)
print(run_radon("cc"))

print("=" * 50)
print("Maintainability index per file (radon mi)")
print("=" * 50)
print(run_radon("mi"))