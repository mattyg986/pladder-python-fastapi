# Deployment Guide

This guide explains how to deploy the Purple Ladder AI Platform using the simplified build and deployment process.

## Project Structure

- `app/` - FastAPI backend code
- `frontend/` - React frontend code
- `Dockerfile` - Universal Docker configuration
- `docker-compose.yml` - Docker Compose configuration
- `deploy.sh` - Unified deployment script

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js 18+
- Railway CLI (for Railway deployments)

## Deployment Options

### 1. Local Development

For local development with hot reloading:

```bash
./deploy.sh development
```

This will:
- Set up Python virtual environment
- Install dependencies
- Build frontend and backend
- Start all services with hot reloading

### 2. Production (Local)

For production-like deployment locally:

```bash
./deploy.sh production
docker-compose up -d
```

This will:
- Build optimized images
- Configure services for production
- Start services in detached mode

### 3. Railway Deployment

For deployment to Railway:

```bash
./deploy.sh railway
```

This will:
- Set up Railway CLI if needed
- Log in to Railway if needed
- Build and deploy to Railway

## Environment Variables

Common environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | - |
| `APP_ENV` | Application environment | `development` |
| `PRODUCTION` | Production mode flag | `false` |
| `DATABASE_URL` | Database connection string | `sqlite:///./app.db` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379/0` |

## Static Files and Frontend Serving

The application uses a multi-stage Docker build to:
1. Build the React frontend in one stage
2. Copy the built files to the FastAPI backend in the next stage

When deployed, the FastAPI server serves both the API and the frontend static files. 
Important notes:

- React creates a nested structure: `app/static/static/{js,css}/main.{js,css}`
- The app mounts the inner static directory to `/static` to serve these files correctly
- Root level files (favicon.ico, manifest.json) have dedicated handlers
- All other frontend routes fall back to index.html for client-side routing

If you modify the frontend or static file serving, make sure to update the paths in `app/main.py`.

## Services

The application consists of:

1. **Web Service** - FastAPI backend serving the React frontend  
   - URL: http://localhost:8000
   - API Docs: http://localhost:8000/docs

2. **Worker Service** - Celery worker for background tasks

3. **Redis** - Message broker for Celery

## Monitoring

- For local deployments: Logs are available in the console
- For Railway: Use `railway logs` to view logs

## Troubleshooting

### Common Issues

1. **Static files not loading in production**
   - Check browser console for 404 errors on specific files
   - Verify the static file paths in app/main.py match the structure in app/static
   - Rebuild the frontend with correct homepage setting in package.json

2. **Memory issues during build**
   - Increase Docker memory limit in Docker Desktop settings
   - Use the development mode that builds frontend locally

3. **Missing dependencies**
   - Make sure all dependencies are installed with `pip install -r requirements.txt`
   - For frontend: `cd frontend && npm install`

4. **Railway deployment fails**
   - Check Railway logs with `railway logs`
   - Make sure environment variables are set in Railway dashboard

### Health Check Issues on Railway

If the health check fails on Railway with "service unavailable" errors:

1. **Check Railway Logs**
   - Run `railway logs` to see application startup errors
   - Look for exceptions, database connection issues, or out-of-memory errors

2. **Verify PORT Environment Variable**
   - Ensure your application is binding to the port provided by Railway via `$PORT`
   - Use the startup script (`startup.sh`) which handles this correctly

3. **Database Connection Issues**
   - If your app relies on a database, ensure the connection string is correct
   - Try making the database initialization fault-tolerant

4. **Memory Constraints**
   - Reduce the number of Gunicorn workers to 2 to avoid memory issues
   - Set appropriate memory limits in railway.json

5. **Check Health Endpoint**
   - Verify `/health` endpoint returns a 200 status code quickly
   - Make sure it doesn't depend on other services that might be unavailable

## Architecture

This deployment uses a multi-stage Docker build:

1. Node.js Alpine stage builds the React frontend with optimizations
2. Python stage runs the FastAPI backend and serves the frontend static files

The FastAPI server handles both API requests and serves the React frontend, simplifying the deployment architecture. 