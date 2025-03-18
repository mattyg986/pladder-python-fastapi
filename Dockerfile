FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./
COPY frontend/.npmrc ./

# Install dependencies with memory optimizations
ENV NODE_OPTIONS="--max-old-space-size=2048"
RUN npm install --production --no-optional --prefer-offline

# Copy frontend source files
COPY frontend/public ./public
COPY frontend/src ./src
COPY frontend/*.js ./

# Build the frontend with optimizations
ENV CI=true
ENV GENERATE_SOURCEMAP=false
RUN npm run build

# Use lightweight Python image for final stage
FROM python:3.9-slim

WORKDIR /app

# Install essential system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application code
COPY app/ ./app/
COPY main.py ./

# Copy frontend build to static directory
COPY --from=frontend-builder /app/build ./app/static

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Default command runs with uvicorn directly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# For production with Gunicorn, override the CMD with:
# CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"] 