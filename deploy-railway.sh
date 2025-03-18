#!/bin/bash
# Script to deploy to Railway with optimizations

set -e  # Exit on any error

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI is not installed. Installing..."
    npm install -g @railway/cli
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

# Remove __pycache__ directories
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Deploy to Railway
echo "==== Deploying to Railway ===="
railway up

echo "==== Railway Deployment Initiated ===="
echo "Check deployment status with: railway status"
echo "View logs with: railway logs" 