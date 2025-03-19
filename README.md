# Pladder Python FastAPI React App

A full-stack application with separate frontend and backend services, using Supabase for authentication.

## Architecture

This application uses a microservices architecture with separate services:

1. **Backend API (FastAPI)**: Provides the REST API for the application
2. **Frontend (React)**: Provides the user interface and handles authentication
3. **Worker (Celery)**: Handles background tasks

## Authentication Flow

The application uses Supabase for authentication:

1. Frontend authenticates users using Supabase client library
2. Authentication tokens are stored securely
3. Backend verifies tokens using JWT verification

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Supabase account (for authentication)
- OpenAI API key (for Agents SDK)

### Environment Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Fill in the required environment variables in the `.env` file:

```
# Required variables
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-key
SUPABASE_JWT_SECRET=your-supabase-jwt-secret
REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Running the Application

We use Docker for both development and production environments:

#### Development Environment

For local development with hot-reloading:

```bash
# Build and start the development environment
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Or to run in detached mode (background)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
```

This starts:
- Frontend with hot reloading at http://localhost:3001
- Backend with auto-reload at http://localhost:8000
- Celery worker for background tasks

#### Production-like Environment

For testing the production setup locally:

```bash
# Build and start the production environment
docker compose up --build

# Or to run in detached mode (background)
docker compose up --build -d
```

### Useful Commands

```bash
# View logs of running containers
docker compose logs -f

# Stop all services
docker compose down

# Run tests
docker compose exec backend pytest
docker compose exec frontend npm test

# Check container status
docker compose ps
```

## API Documentation

When the application is running, you can access the API documentation at:

- http://localhost:8000/api/docs

## Project Structure

```
project-root/
├── frontend/                  # React application
│   ├── public/                # Static assets
│   ├── src/                   # React source code
│   ├── Dockerfile             # Production Dockerfile
│   └── Dockerfile.dev         # Development Dockerfile with hot-reload
│
├── backend/                   # FastAPI application
│   ├── app/                   # Application code
│   │   ├── main.py            # Main FastAPI application
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Core functionality
│   │   └── ...
│   ├── tests/                 # Backend tests
│   └── Dockerfile             # Backend Dockerfile
│
├── docker-compose.yml         # Production Docker Compose config
└── docker-compose.dev.yml     # Development-specific overrides
```

## Deployment

To deploy to Railway:
```bash
# Deploy to Railway (requires Railway CLI)
railway up
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).
