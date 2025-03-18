FROM node:18-slim AS frontend-builder

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./frontend/

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm ci --no-audit --prefer-offline --no-fund

# Copy frontend code
COPY frontend/ ./

# Build the frontend
ENV NODE_OPTIONS="--max-old-space-size=2048"
ENV CI=true
ENV GENERATE_SOURCEMAP=false
RUN npm run build

# Use Python image for the final stage
FROM python:3.9-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

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
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"] 