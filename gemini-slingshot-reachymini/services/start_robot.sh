#!/bin/bash
# ReachyMini Backend Server with Robot Control - Startup Script

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies (including reachy-mini)..."
pip install -r requirements.txt

# Start robot server
echo ""
echo "Starting ReachyMini Robot Server..."
echo "Press Ctrl+C to stop"
echo ""
python3 server_reachymini.py
