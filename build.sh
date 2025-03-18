#!/bin/bash
# Build script for Docker deployment with memory optimizations

set -e  # Exit on any error

echo "==== Docker Build Process Started ===="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"

# Load environment variables if .env.docker exists
if [ -f .env.docker ]; then
    echo "Loading Docker environment variables from .env.docker"
    export $(grep -v '^#' .env.docker | xargs)
fi

# Set default memory values if not already set
DOCKER_MEMORY=${DOCKER_MEMORY:-"4g"}
DOCKER_MEMORY_SWAP=${DOCKER_MEMORY_SWAP:-"6g"}

# Build the Docker image with memory optimizations
echo "==== Building Docker image with memory limits ($DOCKER_MEMORY) ===="
docker build -t pladder-python-fastapi \
    --memory=$DOCKER_MEMORY \
    --memory-swap=$DOCKER_MEMORY_SWAP \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    .

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