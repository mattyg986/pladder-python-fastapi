#!/bin/bash
set -e

echo "Cleaning up directory structure after refactoring..."

# Ensure backend directory structure exists
mkdir -p backend/app

# Copy app contents to backend/app if needed
if [ -d "app" ]; then
    echo "Copying app to backend/app..."
    cp -R app/* backend/app/
    
    echo "Removing duplicate app directory..."
    rm -rf app
fi

# Copy main.py to backend if not already there
if [ -f "main.py" ] && [ ! -f "backend/main.py" ]; then
    echo "Copying main.py to backend..."
    cp main.py backend/
    
    echo "Removing duplicate main.py..."
    rm main.py
fi

# Copy requirements.txt to backend if not already there
if [ -f "requirements.txt" ] && [ ! -f "backend/requirements.txt" ]; then
    echo "Copying requirements.txt to backend..."
    cp requirements.txt backend/
    
    echo "Removing duplicate requirements.txt..."
    rm requirements.txt
fi

# Copy deployment files to backend directory
echo "Organizing deployment files..."

mkdir -p backend/deployment

# Copy startup.sh to backend deployment directory
if [ -f "startup.sh" ]; then
    echo "Moving startup.sh to backend/deployment..."
    cp startup.sh backend/deployment/
    rm startup.sh
fi

# Copy original Dockerfile to backend/deployment for reference
if [ -f "Dockerfile" ]; then
    echo "Moving original Dockerfile to backend/deployment..."
    cp Dockerfile backend/deployment/Dockerfile.original
    rm Dockerfile
fi

# Copy railway.json to backend directory
if [ -f "railway.json" ]; then
    echo "Moving railway.json to backend..."
    cp railway.json backend/
    rm railway.json
fi

# Copy app.json to backend directory
if [ -f "app.json" ]; then
    echo "Moving app.json to backend..."
    cp app.json backend/
    rm app.json
fi

# Copy package.json to root package.json 
if [ -f "package.json" ]; then
    echo "Moving package.json to backend..."
    cp package.json backend/
    
    # Create a monorepo package.json in the root
    cat > package.json << 'EOF'
{
  "name": "pladder-monorepo",
  "version": "1.0.0",
  "private": true,
  "description": "Purple Ladder AI Platform Monorepo",
  "scripts": {
    "start": "docker compose up",
    "build": "docker compose build",
    "start:backend": "cd backend && python -m uvicorn app.main:app --reload",
    "start:frontend": "cd frontend && npm start"
  },
  "workspaces": [
    "frontend"
  ]
}
EOF
fi

# Copy railway configuration files to backend
if [ -f ".railwayignore" ]; then
    echo "Moving .railwayignore to backend..."
    cp .railwayignore backend/
    rm .railwayignore
fi

# Copy .dockerignore to both frontend and backend
if [ -f ".dockerignore" ]; then
    echo "Copying .dockerignore to frontend and backend..."
    cp .dockerignore frontend/
    cp .dockerignore backend/
    
    # Update root .dockerignore for monorepo structure
    cat > .dockerignore << 'EOF'
# Git
.git
.gitignore

# Node.js (for frontend)
**/node_modules
**/npm-debug.log

# Python (for backend)
**/__pycache__
**/*.py[cod]
**/*$py.class
**/*.so
**/.Python
**/env/
**/build/
**/develop-eggs/
**/dist/
**/downloads/
**/eggs/
**/.eggs/
**/lib/
**/lib64/
**/parts/
**/sdist/
**/var/
**/wheels/
**/*.egg-info/
**/.installed.cfg
**/*.egg

# Virtual Environment
**/venv
**/env
**/.env
**/.venv
**/ENV

# IDEs and editors
**/.idea
**/.vscode
**/*.swp
**/*.swo

# OS specific
.DS_Store
Thumbs.db
EOF
fi

# Update DEPLOYMENT.md in the root
if [ -f "DEPLOYMENT.md" ]; then
    echo "Updating DEPLOYMENT.md for new architecture..."
    cp DEPLOYMENT.md backend/deployment/DEPLOYMENT.original.md
    
    cat > DEPLOYMENT.md << 'EOF'
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
EOF
fi

# Copy deploy.sh to the project root with updates
if [ -f "deploy.sh" ]; then
    echo "Updating deploy.sh..."
    cat > deploy.sh << 'EOF'
#!/bin/bash
# Unified deployment script for separated frontend and backend

set -e  # Exit on any error

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to development mode
DEPLOY_ENV=${1:-development}

echo -e "${BLUE}=== Purple Ladder AI Platform Deployment ===${NC}"
echo -e "${YELLOW}Environment: ${DEPLOY_ENV}${NC}"

# Clean up
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

case $DEPLOY_ENV in
    development)
        echo -e "${GREEN}Starting local development environment...${NC}"
        
        # Check for Python virtual environment for backend
        if [ ! -d "backend/venv" ]; then
            echo -e "${YELLOW}Creating Python virtual environment for backend...${NC}"
            (cd backend && python3 -m venv venv)
        fi
        
        # Install backend Python dependencies
        echo -e "${YELLOW}Installing backend Python dependencies...${NC}"
        (cd backend && source venv/bin/activate && pip install -r requirements.txt)
        
        # Install frontend dependencies
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        (cd frontend && npm install)
        
        # Start with docker compose for development
        echo -e "${GREEN}Starting services with Docker Compose...${NC}"
        export APP_ENV=development
        export PRODUCTION=false
        
        # Build and start services
        docker compose up --build
        ;;
        
    production)
        echo -e "${GREEN}Starting production deployment...${NC}"
        
        # Build for production with docker compose
        echo -e "${YELLOW}Building for production...${NC}"
        export APP_ENV=production
        export PRODUCTION=true
        
        docker compose build
        
        echo -e "${GREEN}Production build completed.${NC}"
        echo -e "${YELLOW}To start services: docker compose up -d${NC}"
        ;;
        
    railway)
        echo -e "${GREEN}Deploying to Railway...${NC}"
        
        # Check if Railway CLI is installed
        if ! command -v railway &> /dev/null; then
            echo -e "${YELLOW}Railway CLI not found. Installing...${NC}"
            npm install -g @railway/cli || npm install @railway/cli
            export PATH="$PATH:./node_modules/.bin"
        fi
        
        # Check if logged in to Railway
        if ! railway whoami &> /dev/null; then
            echo -e "${YELLOW}Please log in to Railway:${NC}"
            railway login
        fi
        
        # Set production environment variables
        echo -e "${YELLOW}Setting production environment variables...${NC}"
        railway variables set PRODUCTION=true
        
        # Deploy to Railway
        echo -e "${YELLOW}Deploying to Railway...${NC}"
        railway up --detach
        
        echo -e "${GREEN}Railway deployment initiated.${NC}"
        echo -e "${YELLOW}Check status with: railway status${NC}"
        echo -e "${YELLOW}View logs with: railway logs${NC}"
        ;;
        
    *)
        echo -e "${RED}Unknown environment: ${DEPLOY_ENV}${NC}"
        echo -e "${YELLOW}Usage: ./deploy.sh [development|production|railway]${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}=== Deployment process completed ===${NC}"
EOF
    chmod +x deploy.sh
fi

# Copy test files to backend/tests directory
mkdir -p backend/tests
if [ -f "test_agents_sdk.py" ] || [ -f "test_agents_sdk_api.py" ] || [ -f "test_assistant.py" ]; then
    echo "Moving test files to backend/tests..."
    [ -f "test_agents_sdk.py" ] && cp test_agents_sdk.py backend/tests/ && rm test_agents_sdk.py
    [ -f "test_agents_sdk_api.py" ] && cp test_agents_sdk_api.py backend/tests/ && rm test_agents_sdk_api.py
    [ -f "test_assistant.py" ] && cp test_assistant.py backend/tests/ && rm test_assistant.py
fi

# Move tests directory to backend if it exists
if [ -d "tests" ] && [ ! -d "backend/tests" ]; then
    echo "Moving tests directory to backend..."
    cp -R tests/* backend/tests/
    rm -rf tests
fi

# Move migrations directory to backend if it exists
if [ -d "migrations" ] && [ ! -d "backend/migrations" ]; then
    echo "Moving migrations directory to backend..."
    cp -R migrations backend/
    rm -rf migrations
fi

# Create frontend/nginx.conf if it doesn't exist
if [ ! -f "frontend/nginx.conf" ]; then
    echo "Creating frontend/nginx.conf..."
    cat > frontend/nginx.conf << 'EOF'
server {
    listen 80;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API requests to the backend
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Serve static files with cache headers
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        root /usr/share/nginx/html;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
        try_files $uri =404;
    }
    
    # Error pages
    error_page 404 /index.html;
    error_page 500 502 503 504 /index.html;
}
EOF
fi

# Make sure backend Dockerfile exists
if [ ! -f "backend/Dockerfile" ]; then
    echo "Creating backend/Dockerfile..."
    cat > backend/Dockerfile << 'EOF'
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir PyJWT==2.6.0

# Copy app code
COPY app/ ./app/
COPY main.py ./

# Set environment variables
ENV PYTHONPATH="/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
fi

# Update the .env.example file in the root with correct paths
echo "Updating .env.example..."
cat > .env.example << 'EOF'
# Application Configuration
APP_ENV=development
PRODUCTION=false

# OpenAI API Key (Required for Agents SDK)
OPENAI_API_KEY=your_openai_api_key_here

# Redis Configuration
# For development, use the Railway Redis URL
# In production on Railway, the Redis service is connected automatically
REDIS_URL=redis://default:password@metro.proxy.rlwy.net:port/0

# Supabase Configuration - Backend
# These are used by the FastAPI backend to interact with Supabase
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-key
SUPABASE_JWT_SECRET=your-supabase-jwt-secret

# Supabase Configuration - Frontend
# These are used by the React frontend for client-side authentication
REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key

# Frontend API URL - The URL where the FastAPI backend can be reached by the frontend
REACT_APP_API_URL=http://localhost:8000

# Docker Compose configuration
CELERY_CONCURRENCY=2

# For production deployment on Railway
PORT=8000
EOF

echo "Cleanup complete. You can now start the application with docker compose up"
echo "Directory structure:"
echo ""
find . -maxdepth 1 -type f | sort
echo ""
find . -type d -maxdepth 2 | sort 