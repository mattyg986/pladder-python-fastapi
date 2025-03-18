#!/bin/bash
# Development script for the Purple Ladder AI Agents Platform

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Starting Purple Ladder AI Agents Platform in Development Mode ===${NC}"

# Check for Python virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}Virtual environment activated.${NC}"

# Install Python dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    touch venv/.dependencies_installed
    echo -e "${GREEN}Python dependencies installed.${NC}"
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend && npm install && cd ..
    echo -e "${GREEN}Frontend dependencies installed.${NC}"
fi

# Start Redis
echo -e "${YELLOW}Starting Redis...${NC}"
brew services start redis
echo -e "${GREEN}Redis started.${NC}"

# Start the development servers
echo -e "${YELLOW}Starting servers in development mode...${NC}"

# Create logs directory
mkdir -p logs

# Start Celery worker
echo -e "${YELLOW}Starting Celery worker...${NC}"
celery -A app.worker worker --loglevel=info --concurrency=2 > logs/celery.log 2>&1 &
CELERY_PID=$!
echo -e "${GREEN}Celery worker started (PID: $CELERY_PID).${NC}"

# Start FastAPI backend
echo -e "${YELLOW}Starting backend server...${NC}"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started (PID: $BACKEND_PID).${NC}"

# Start React frontend
echo -e "${YELLOW}Starting frontend server...${NC}"
cd frontend && npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}Frontend server started (PID: $FRONTEND_PID).${NC}"

# Summary
echo -e "\n${GREEN}=== All Services Started (Development Mode) ===${NC}"
echo -e "${GREEN}Redis:${NC} Running on port 6379"
echo -e "${GREEN}Celery:${NC} Running in background (PID: $CELERY_PID, logs: logs/celery.log)"
echo -e "${GREEN}Backend:${NC} Running on http://localhost:8000 (PID: $BACKEND_PID, logs: logs/backend.log)"
echo -e "${GREEN}Frontend:${NC} Running on http://localhost:3000 (PID: $FRONTEND_PID, logs: logs/frontend.log)"
echo -e "\n${GREEN}Access the platform at:${NC} http://localhost:3000"
echo -e "${GREEN}API documentation at:${NC} http://localhost:8000/docs"
echo -e "\n${YELLOW}To stop all services, run: ./stop.sh${NC}"

# Trap for CTRL+C
trap "echo -e '${YELLOW}Stopping servers...${NC}'; ./stop.sh; exit" INT
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for Ctrl+C
while true; do
    sleep 1
done 