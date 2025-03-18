#!/bin/bash
# Build script for Docker deployment

set -e  # Exit on any error

echo "==== Docker Build Process Started ===="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"

# Build the Docker image
echo "==== Building Docker image ===="
docker build -t pladder-python-fastapi .

echo "==== Docker image built successfully! ===="

# Optionally run the containers
if [ "$1" == "--run" ]; then
    echo "==== Starting containers with Docker Compose ===="
    docker-compose up -d
    echo "==== Application is running! ===="
    echo "Access the application at http://localhost:8000"
fi

echo "==== Build completed successfully! ===="
echo "To start the application, run: docker-compose up -d" 