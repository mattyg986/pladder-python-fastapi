FROM node:18-slim AS frontend-builder

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./frontend/

# Install frontend dependencies with memory optimization flags
WORKDIR /app/frontend
# Optimize npm installation to use less memory
ENV NODE_OPTIONS="--max-old-space-size=2048"
RUN npm ci --no-audit --prefer-offline --no-fund --production && \
    npm install --no-save --no-audit --prefer-offline react-scripts

# Copy frontend code
COPY frontend/ ./

# Build the frontend with memory optimization
ENV CI=true
ENV GENERATE_SOURCEMAP=false
RUN npm run build

# Use Python image for the final stage
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libffi-dev g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies in smaller batches to avoid memory issues
COPY requirements.txt .
RUN pip install --no-cache-dir setuptools wheel && \
    grep -v "openai" requirements.txt > requirements_base.txt && \
    pip install --no-cache-dir -r requirements_base.txt && \
    grep "openai" requirements.txt > requirements_openai.txt && \
    pip install --no-cache-dir -r requirements_openai.txt && \
    rm requirements_base.txt requirements_openai.txt

# Copy backend code
COPY app/ ./app/

# Create static directory and copy frontend build
RUN mkdir -p ./app/static
COPY --from=frontend-builder /app/frontend/build/ ./app/static/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RAILWAY_ENVIRONMENT=production

# Expose port
EXPOSE 8000

# Command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 