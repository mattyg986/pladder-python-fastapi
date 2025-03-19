#!/bin/bash
# Deployment script for development and production environments

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
        echo -e "${GREEN}Starting development environment with Docker...${NC}"
        
        # Set environment variables
        export APP_ENV=development
        export PRODUCTION=false
        
        # Build and start services with dev configuration
        docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
        ;;
        
    production)
        echo -e "${GREEN}Starting production deployment with Docker...${NC}"
        
        # Set environment variables
        export APP_ENV=production
        export PRODUCTION=true
        
        # Build and start services
        docker compose up --build -d
        
        echo -e "${GREEN}Production deployment completed.${NC}"
        echo -e "${YELLOW}To view logs: docker compose logs -f${NC}"
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
