#!/bin/bash

echo "Preparing server to launch!"

cd server/

# Setup python virtual env and dependencies if not setup already
if [ -d "./.venv" ]; then
    echo "Python virtual environment already setup!"
    
    # Activate the virtual env 
    . .venv/bin/activate
else
    # Install the virtual environments
    python3 -m venv .venv

    # Install dependencies
    . .venv/bin/activate
    pip install -r requirements.txt
fi


# Run server applications
python3 server.py