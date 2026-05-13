COS730 Assignment 2
This repo contains my code for COS730 Assignment 2.
Folder structure:

Original/ — Task 1 baseline implementation
Optimised/ — Task 5 optimised implementation

Each folder is self contained.
Running the systems:
cd Original
python main.py
or
cd Optimised
python main.py
Both systems run the same four scenarios: invalid, accept, reject and revision. The inboxes at the end of each scenario match across the two systems.

Benchmark:
I wrote a benchmark script for Task 6 which lives in both folders. It needs the radon library:
pip install radon
Then run it the same way:
cd Original or cd Optimised
python benchmark.py
It prints method call counts, execution times, cyclomatic complexity and the maintainability index for the system it is in.

Tested on: Python 3.10.11, Windows 11.