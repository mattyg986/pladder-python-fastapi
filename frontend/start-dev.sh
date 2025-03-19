#!/bin/bash

# Load environment variables from root .env file
echo "Loading environment variables from root .env file..."
export $(grep -v '^#' ../.env | xargs)

# Start the React development server
echo "Starting React development server..."
npm start 