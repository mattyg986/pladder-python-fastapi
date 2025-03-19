#!/bin/bash
set -e

# Load environment variables from .env file
if [ -f "../.env" ]; then
  echo "Loading environment variables from ../.env"
  export $(grep -v '^#' ../.env | xargs)
fi

# Load development-specific variables
if [ -f ".env.development" ]; then
  echo "Loading environment variables from .env.development"
  export $(grep -v '^#' .env.development | xargs)
fi

# Start the development server
echo "Starting React development server..."
npm start 