#!/bin/bash
# Simple build script for Railway

set -e  # Exit on any error

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing frontend dependencies..."
cd frontend
npm ci

echo "Building frontend..."
npm run build

echo "Setting up static files..."
mkdir -p ../app/static
cp -r build/* ../app/static/
cd ..

echo "Build completed successfully!" 