#! /usr/bin/env bash

# Location: backend/prestart.sh

export PYTHONPATH=/backend:$PYTHONPATH

# Run any pre-start scripts if needed
# python /backend/app/pre_start.py

# Create initial data in DB
python /backend/app/initial_data.py