#!/bin/bash

rm *sage.py

for solver in *.py; do
    echo "Running ------------------------ $solver --------------------------"
    python3 $solver
done

for solver in *.sage; do
    echo "Running ------------------------ $solver --------------------------"
    sage $solver
done

npm install --silent

for solver in *.js; do
    echo "Running ------------------------ $solver --------------------------"
    node $solver
done
