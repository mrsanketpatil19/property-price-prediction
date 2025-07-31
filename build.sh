#!/bin/bash

# Upgrade pip
python3 -m pip install --upgrade pip

# Install requirements
pip3 install -r requirements.txt

# Check if model files exist
if [ ! -f "model.pkl" ]; then
    echo "Warning: model.pkl not found"
fi

if [ ! -f "scaler.pkl" ]; then
    echo "Warning: scaler.pkl not found"
fi

if [ ! -f "feature_columns.pkl" ]; then
    echo "Warning: feature_columns.pkl not found"
fi

echo "Build completed successfully" 