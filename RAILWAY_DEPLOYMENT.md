# Railway Deployment Guide

This guide explains how to deploy this Python FastAPI and React application to Railway.

## Prerequisites

- [Railway CLI](https://docs.railway.app/develop/cli) installed
- Railway account and project set up
- Git repository cloned locally

## Project Structure

- `app/` - FastAPI backend
- `frontend/` - React frontend
- `railway.Dockerfile` - Docker configuration for Railway
- `railway.json` - Railway project configuration
- `.railwayignore` - Files to exclude from Railway
- `deploy-railway.sh` - Deployment script

## Deployment Steps

### 1. Prepare the Application

Make sure your codebase is clean and ready for deployment:

```bash
# Clean unnecessary files
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### 2. Manual Deployment

```bash
# Login to Railway
railway login

# Deploy using the script
./deploy-railway.sh
```

The deployment script will:
- Clean up unnecessary files
- Create required directories
- Deploy to Railway

### 3. Monitor Deployment

```bash
# Check deployment status
railway status

# View deployment logs
railway logs
```

## Configuration

### Environment Variables

Set these in your Railway project:

- `OPENAI_API_KEY` - Your OpenAI API key
- `DATABASE_URL` - Auto-provided by Railway PostgreSQL plugin
- `REDIS_URL` - Auto-provided by Railway Redis plugin
- `RAILWAY_ENVIRONMENT` - Set to "production"

### Services

This project requires:
- PostgreSQL
- Redis (for Celery)

Add these services through the Railway dashboard.

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Docker build logs for specific errors
   - Ensure all required files are included in the repository

2. **Runtime Errors**
   - Check application logs using `railway logs`
   - Verify environment variables are set correctly

3. **Deployment Timeout**
   - Increase the `healthcheckTimeout` in railway.json

## Maintenance

To update your deployment:

1. Make changes to your codebase
2. Commit changes to Git
3. Run the deployment script:
   ```bash
   ./deploy-railway.sh
   ```

## Architecture

This deployment uses a multi-stage Docker build:
1. Node.js stage builds the React frontend
2. Python stage runs the FastAPI backend and serves the frontend static files

The FastAPI server handles both API requests and serves the React frontend, simplifying the deployment architecture. 