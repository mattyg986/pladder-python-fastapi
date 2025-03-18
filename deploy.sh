#!/bin/bash
# Unified deployment script for local and Railway environments

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

# Ensure app/static directory exists
if [ ! -d "app/static" ]; then
    echo -e "${YELLOW}Creating app/static directory...${NC}"
    mkdir -p app/static
    touch app/static/.gitkeep
fi

case $DEPLOY_ENV in
    development)
        echo -e "${GREEN}Starting local development environment...${NC}"
        
        # Check for Python virtual environment
        if [ ! -d "venv" ]; then
            echo -e "${YELLOW}Creating Python virtual environment...${NC}"
            python3 -m venv venv
        fi
        
        # Activate virtual environment
        echo -e "${YELLOW}Activating virtual environment...${NC}"
        source venv/bin/activate
        
        # Install Python dependencies
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        pip install -r requirements.txt
        
        # Start with docker-compose for development
        echo -e "${GREEN}Starting services with Docker Compose...${NC}"
        export APP_ENV=development
        export PRODUCTION=false
        export MOUNT_APP=./app:/app/app
        export WEB_COMMAND="uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
        
        # Build and start services
        docker-compose up --build
        ;;
        
    production)
        echo -e "${GREEN}Starting production deployment...${NC}"
        
        # Build for production with docker-compose
        echo -e "${YELLOW}Building for production...${NC}"
        export APP_ENV=production
        export PRODUCTION=true
        export MOUNT_APP=./app:/app/app:ro
        export WEB_COMMAND="gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app"
        
        docker-compose build
        
        echo -e "${GREEN}Production build completed.${NC}"
        echo -e "${YELLOW}To start services: docker-compose up -d${NC}"
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