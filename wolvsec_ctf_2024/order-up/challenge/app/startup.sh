#!/bin/bash
postgres&

sleep 10

python3 -m flask run --host=0.0.0.0