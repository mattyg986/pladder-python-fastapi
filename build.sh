#!/bin/bash
# Enhanced build script for Railway

set -e  # Exit on any error

echo "==== Build Process Started ===="
echo "Environment: $RAILWAY_ENVIRONMENT"
echo "Node version: $(node -v)"
echo "NPM version: $(npm -v)"
echo "Python version: $(python --version)"

echo "==== Installing Python dependencies ===="
pip install -r requirements.txt

echo "==== Creating static directory ===="
mkdir -p app/static
touch app/static/.gitkeep

echo "==== Checking frontend directory ===="
ls -la frontend

echo "==== Installing frontend dependencies ===="
cd frontend
# Use --no-audit to reduce memory usage
npm ci --no-audit --prefer-offline --no-fund

# Memory optimization for React build
export NODE_OPTIONS="--max-old-space-size=2048"

echo "==== Building frontend with optimizations ===="
# Use production flag to reduce build size
npm run build -- --profile

echo "==== Copying built files to static directory ===="
ls -la build
cp -rv build/* ../app/static/
cd ..

echo "==== Checking static directory ===="
ls -la app/static

echo "==== Build completed successfully! ====" 