# Multi-stage build

# Stage 1: Build the frontend
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend
WORKDIR /app

# Copy frontend package.json and lock file
COPY frontend/package*.json ./
COPY frontend/.npmrc ./

# Install frontend dependencies 
RUN npm install --production --no-optional --prefer-offline

# Copy frontend source code
COPY frontend/public ./public
COPY frontend/src ./src

# Copy other frontend configuration files
COPY frontend/*.js ./

# Pass environment variables for Supabase
ARG REACT_APP_SUPABASE_URL
ARG REACT_APP_SUPABASE_ANON_KEY
ENV REACT_APP_SUPABASE_URL=${REACT_APP_SUPABASE_URL}
ENV REACT_APP_SUPABASE_ANON_KEY=${REACT_APP_SUPABASE_ANON_KEY}

# Hard-code Supabase URLs for local development when not set
ENV REACT_APP_SUPABASE_URL=${REACT_APP_SUPABASE_URL:-https://dyfnqcybcnvuhxreflqu.supabase.co}
ENV REACT_APP_SUPABASE_ANON_KEY=${REACT_APP_SUPABASE_ANON_KEY:-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5Zm5xY3liY252dWh4cmVmbHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk5MzM4MzYsImV4cCI6MjA1NTUwOTgzNn0.eq0vCqZXghv1U-ANCuGGJWi6LYTuxxEqhdtEgPY_PSE}

# Build the React app
RUN npm run build

# Stage 2: Set up the Python application
FROM python:3.9-slim

# Set working directory for backend
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
    pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app/

# Copy main file
COPY main.py ./

# Copy startup script
COPY startup.sh ./
RUN chmod +x startup.sh

# Copy frontend build from the frontend-builder stage
COPY --from=frontend-builder /app/build ./app/static

# Create the static directory and set permissions
RUN mkdir -p ./app/static && chmod -R 755 ./app/static

# Set environment variables
ENV PYTHONPATH="/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["./startup.sh"] 