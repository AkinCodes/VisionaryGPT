#!/bin/bash

# Load conda shell functions
eval "$(conda shell.bash hook)"

# Activate the vision-env environment
conda activate vision-env

# Set PYTHONPATH and run the FastAPI server
export PYTHONPATH=$(pwd)/backend
/Users/akin.olusanya/anaconda3/envs/vision-env/bin/python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
