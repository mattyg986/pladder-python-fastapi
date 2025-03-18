#!/bin/bash
# Stop script for the Purple Ladder AI Agents Platform

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping all services...${NC}"

# Stop frontend (React)
pkill -f 'react-scripts start' 2>/dev/null
echo -e "${GREEN}Frontend server stopped.${NC}"

# Stop backend (FastAPI)
pkill -f 'uvicorn app.main:app' 2>/dev/null
echo -e "${GREEN}Backend server stopped.${NC}"

# Stop Celery worker
pkill -f 'celery' 2>/dev/null
echo -e "${GREEN}Celery worker stopped.${NC}"

# Stop Redis
brew services stop redis
echo -e "${GREEN}Redis stopped.${NC}"

echo -e "${GREEN}All services have been stopped.${NC}" 