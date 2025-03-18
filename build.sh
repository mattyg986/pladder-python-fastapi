#!/bin/bash
# Production build script for the Purple Ladder AI Agents Platform

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Building Purple Ladder AI Agents Platform for Production ===${NC}"

# Check for environment variables
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}Warning: OPENAI_API_KEY environment variable not set.${NC}"
    echo -e "${YELLOW}AI features may not work properly in production.${NC}"
fi

# Create and activate Python virtual environment if not in a production environment
if [ -z "$RAILWAY_ENVIRONMENT" ]; then
    echo -e "${YELLOW}Setting up Python environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}Python environment activated.${NC}"
fi

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}Python dependencies installed.${NC}"

# Build frontend
echo -e "${YELLOW}Building frontend...${NC}"
cd frontend
npm install
npm run build
echo -e "${GREEN}Frontend built successfully.${NC}"

# Create static directory in backend
echo -e "${YELLOW}Setting up static files...${NC}"
mkdir -p ../app/static
cp -r build/* ../app/static/
cd ..
echo -e "${GREEN}Static files set up successfully.${NC}"

# Set Railway environment variable for local testing
export RAILWAY_ENVIRONMENT=production

echo -e "${GREEN}Build completed successfully!${NC}"
echo -e "${YELLOW}You can now start the application with: uvicorn app.main:app --host 0.0.0.0 --port \$PORT${NC}" 