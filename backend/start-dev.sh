#!/bin/bash
set -e

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Load environment variables from .env file
if [ -f "../.env" ]; then
  echo "Loading environment variables from ../.env"
  export $(grep -v '^#' ../.env | xargs)
fi

# Set development-specific environment variables
export APP_ENV=development
export PRODUCTION=false
export BYPASS_AUTH=${BYPASS_AUTH:-false}

# Start the development server
echo "Starting FastAPI development server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 