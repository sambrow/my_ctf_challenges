#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

python3 $SCRIPT_DIR/../solvers/solver-for-filter-madness.py
python3 $SCRIPT_DIR/../solvers/solver-for-hidden-css.py
python3 $SCRIPT_DIR/../solvers/solver-for-zombie-101.py
python3 $SCRIPT_DIR/../solvers/solver-for-zombie-201.py
python3 $SCRIPT_DIR/../solvers/solver-for-zombie-301.py
python3 $SCRIPT_DIR/../solvers/solver-for-zombie-401.py

