FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy frontend directory with package files
COPY frontend/package*.json ./
COPY frontend/.npmrc ./

# Install dependencies with production optimization
ENV NODE_OPTIONS="--max-old-space-size=3072"
RUN npm ci --only=production --no-audit --prefer-offline

# Copy only what's needed for the build
COPY frontend/public ./public
COPY frontend/src ./src
COPY frontend/*.js ./

# Build with optimization
ENV CI=true
ENV GENERATE_SOURCEMAP=false
RUN npm run build

# Use lightweight Python image for final stage
FROM python:3.9-slim

WORKDIR /app

# Install only essential system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies in optimized way
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy only what's needed for the application
COPY app/ ./app/
COPY main.py ./

# Create static directory and copy frontend build
COPY --from=frontend-builder /app/build ./app/static

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RAILWAY_ENVIRONMENT=production
ENV PORT=8000

# Expose port
EXPOSE 8000

# Start with Gunicorn for better performance
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app 