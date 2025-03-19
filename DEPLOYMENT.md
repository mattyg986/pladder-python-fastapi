# Deployment Guide for Purple Ladder AI Platform

This document outlines how to deploy the Purple Ladder AI Platform using our new microservices architecture.

## Architecture Overview

The application is split into three main services:

1. **Frontend (React)**: User interface with Supabase authentication
2. **Backend (FastAPI)**: API server with JWT validation
3. **Worker (Celery)**: Background task processing

## Local Development

### Option 1: Using Docker Compose (Recommended)

The simplest way to run the entire application:

```bash
# Clone the repository
git clone https://github.com/yourusername/pladder-python-fastapi.git
cd pladder-python-fastapi

# Copy the environment file and update with your keys
cp .env.example .env

# Start all services
docker compose up
```

This will start:
- Backend API at http://localhost:8000
- Frontend at http://localhost:3000
- Celery worker for background tasks
- Redis server for message broker

### Option 2: Running Services Individually

For more flexibility during development:

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## Production Deployment

### Railway Deployment

The application is configured for easy deployment to Railway:

1. Install the Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to your Railway account:
   ```bash
   railway login
   ```

3. Link to your project:
   ```bash
   railway link
   ```

4. Deploy the application:
   ```bash
   ./deploy.sh railway
   ```

## Environment Variables

Make sure to set these environment variables in your Railway project:

- `OPENAI_API_KEY`: Your OpenAI API key
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase service role key
- `SUPABASE_JWT_SECRET`: JWT secret from Supabase project settings
- `REACT_APP_SUPABASE_URL`: Same as SUPABASE_URL
- `REACT_APP_SUPABASE_ANON_KEY`: Supabase anon/public key

## Detailed Documentation

For more information about each service:
- Backend: See `backend/README.md`
- Frontend: See `frontend/README.md`
