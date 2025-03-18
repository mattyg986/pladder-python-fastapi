# Docker Deployment Guide for Purple Ladder AI Agents Platform

This guide outlines how to build, run, and deploy the Purple Ladder AI Agents Platform using Docker.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine
- OpenAI API key

## Local Development with Docker

### Building the Docker Image

You can build the Docker image using the provided build script:

```bash
./build.sh
```

Or manually with Docker:

```bash
docker build -t pladder-python-fastapi .
```

### Running the Application

Start the application with Docker Compose:

```bash
docker-compose up -d
```

This will:
1. Start a Redis container
2. Build and start the application container

The application will be available at http://localhost:8000

To stop the application:

```bash
docker-compose down
```

## Deployment to Railway

### Preparation

1. Make sure your code is committed to a Git repository
2. Sign up for a Railway account at https://railway.app
3. Connect your repository to Railway

### Configuration

The application is already configured for Railway deployment with the `railway.json` file:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300
  }
}
```

### Environment Variables

In your Railway project, add the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `RAILWAY_ENVIRONMENT`: Set to `production`
- `SECRET_KEY`: A secure random string for encryption

### Adding a Redis Service

1. In your Railway project, click "New Service"
2. Select "Redis"
3. Railway will automatically inject the `REDIS_URL` environment variable

### Deploying

1. Push your changes to your Git repository
2. Railway will automatically build and deploy the application
3. Access the application at the URL provided by Railway

## Dockerfile Explanation

The Dockerfile uses a multi-stage build:

1. **Stage 1: Frontend Build**
   - Uses Node.js 18 to build the React frontend
   - Optimizes the build for production

2. **Stage 2: Backend**
   - Uses Python 3.9 for the FastAPI backend
   - Copies the built frontend from Stage 1
   - Sets up environment variables
   - Exposes port 8000
   - Starts the application with Uvicorn

## Docker Compose Explanation

The docker-compose.yml file defines:

1. **Web Service**
   - Builds the application using the Dockerfile
   - Maps port 8000 to the host
   - Sets environment variables
   - Depends on Redis

2. **Redis Service**
   - Uses the official Redis Alpine image
   - Maps port 6379 to the host
   - Uses a volume for data persistence

## Troubleshooting

**Docker Build Fails**
- Make sure Docker daemon is running
- Check if you have enough disk space
- Verify that all required files are in the repository

**Memory-Related Build Failures**
- If you see errors like `exit code: 137` or npm install failures, your build is running out of memory
- Use the provided `.env.docker` file to increase memory allocation
- For local builds, ensure Docker has sufficient memory allocated in Docker Desktop preferences
- For Railway, the `railway.json` file has been configured with memory optimizations

**Application Doesn't Start**
- Check Docker logs: `docker-compose logs`
- Verify environment variables are properly set
- Ensure Redis is running correctly

**Railway Deployment Issues**
- Check Railway logs in the dashboard
- Verify environment variables are properly set
- Check if the health check endpoint is working 