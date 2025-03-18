#!/bin/bash
# Unified startup script for the Purple Ladder AI Agents Platform
# This script manages the startup of Redis, Celery, FastAPI backend, and React frontend

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Configuration
VENV_PATH="./venv"
BACKEND_PORT=8000
FRONTEND_PORT=3000
REDIS_PORT=6379

echo -e "${GREEN}=== Purple Ladder AI Agents Platform Startup ===${NC}"

# Check for Python virtual environment
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv $VENV_PATH
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate virtual environment
source $VENV_PATH/bin/activate
echo -e "${GREEN}Virtual environment activated.${NC}"

# Check and install dependencies
echo -e "${YELLOW}Checking backend dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}Backend dependencies installed.${NC}"

# Check if .env file exists with OpenAI API key
if [ ! -f ".env" ] || ! grep -q "OPENAI_API_KEY" .env; then
    echo -e "${RED}WARNING: OpenAI API key not found in .env file.${NC}"
    echo -e "${YELLOW}AI features may not work properly.${NC}"
fi

# Function to check if a port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Function to kill a process running on a specific port
kill_port_process() {
    echo -e "${YELLOW}Stopping process on port $1...${NC}"
    lsof -ti :$1 | xargs kill -9 2>/dev/null
    sleep 1
    echo -e "${GREEN}Process on port $1 stopped.${NC}"
}

# Step 1: Check and start Redis
echo -e "${YELLOW}Checking Redis...${NC}"
if brew services info redis | grep -q "started"; then
    echo -e "${GREEN}Redis is already running. Restarting...${NC}"
    brew services restart redis
else
    echo -e "${YELLOW}Starting Redis...${NC}"
    brew services start redis
fi
echo -e "${GREEN}Redis started successfully.${NC}"

# Step 2: Stop any existing Celery processes
echo -e "${YELLOW}Checking for Celery processes...${NC}"
pkill -f 'celery' 2>/dev/null
echo -e "${GREEN}Celery processes stopped (if any were running).${NC}"

# Step 3: Stop any existing backend server
if check_port $BACKEND_PORT; then
    kill_port_process $BACKEND_PORT
    echo -e "${GREEN}Backend server stopped.${NC}"
else
    echo -e "${GREEN}No backend server running on port $BACKEND_PORT.${NC}"
fi

# Step 4: Stop any existing frontend server
if check_port $FRONTEND_PORT; then
    kill_port_process $FRONTEND_PORT
    echo -e "${GREEN}Frontend server stopped.${NC}"
else
    echo -e "${GREEN}No frontend server running on port $FRONTEND_PORT.${NC}"
fi

# Step 5: Start Celery worker in the background
echo -e "${YELLOW}Starting Celery worker...${NC}"
mkdir -p logs
celery -A app.worker worker --loglevel=info --concurrency=2 > logs/celery.log 2>&1 &
CELERY_PID=$!
echo -e "${GREEN}Celery worker started (PID: $CELERY_PID).${NC}"

# Step 6: Start FastAPI backend in the background
echo -e "${YELLOW}Starting backend server...${NC}"
mkdir -p logs
uvicorn app.main:app --reload --host 0.0.0.0 --port $BACKEND_PORT > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started (PID: $BACKEND_PID).${NC}"

# Give the backend a moment to start
sleep 2

# Step 7: Start React frontend in the background
echo -e "${YELLOW}Starting frontend server...${NC}"
cd frontend && npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}Frontend server started (PID: $FRONTEND_PID).${NC}"

# Summary
echo -e "\n${GREEN}=== All Services Started ===${NC}"
echo -e "${GREEN}Redis:${NC} Running on port $REDIS_PORT"
echo -e "${GREEN}Celery:${NC} Running in background (PID: $CELERY_PID, logs: logs/celery.log)"
echo -e "${GREEN}Backend:${NC} Running on http://localhost:$BACKEND_PORT (PID: $BACKEND_PID, logs: logs/backend.log)"
echo -e "${GREEN}Frontend:${NC} Running on http://localhost:$FRONTEND_PORT (PID: $FRONTEND_PID, logs: logs/frontend.log)"
echo -e "\n${GREEN}Access the platform at:${NC} http://localhost:$FRONTEND_PORT"
echo -e "${GREEN}API documentation at:${NC} http://localhost:$BACKEND_PORT/docs"
echo -e "\n${YELLOW}To stop all services, run: ./stop.sh${NC}"

# Create a stop script
cat > stop.sh << 'EOF'
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
EOF

chmod +x stop.sh
chmod +x start.sh

echo -e "${YELLOW}Created stop.sh script to stop all services.${NC}" 