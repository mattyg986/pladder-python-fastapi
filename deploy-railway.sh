#!/bin/bash
# Script to deploy to Railway with optimizations

set -e  # Exit on any error

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI is not installed. Installing..."
    npm install -g @railway/cli --no-fund --silent || npm install @railway/cli --no-fund --silent
    
    # If global install failed, add npm bin to PATH temporarily
    if ! command -v railway &> /dev/null; then
        echo "Adding local npm bin to PATH for this session..."
        export PATH="$PATH:./node_modules/.bin"
    fi
fi

echo "==== Railway Deployment Process Started ===="

# Check if user is logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "Not logged in to Railway. Please log in:"
    railway login
fi

# Clean up any unnecessary files before deploying
echo "==== Cleaning up repository for faster deployment ===="
# Remove node_modules if it exists
if [ -d "frontend/node_modules" ]; then
    echo "Removing frontend/node_modules for faster snapshot..."
    rm -rf frontend/node_modules
fi

# Remove __pycache__ directories and .pyc files
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Make sure app/static directory exists
if [ ! -d "app/static" ]; then
    echo "Creating app/static directory..."
    mkdir -p app/static
    touch app/static/.gitkeep
fi

# Deploy to Railway
echo "==== Deploying to Railway ===="
railway up --detach

echo "==== Railway Deployment Initiated ===="
echo "Check deployment status with: railway status"
echo "View logs with: railway logs" 