#!/bin/bash
set -e

# Log environment information for debugging
echo "Starting application..."
echo "PORT: $PORT"
echo "APP_ENV: $APP_ENV"
echo "PRODUCTION: $PRODUCTION"

# Ensure environment variables are set properly
export PRODUCTION=true
export APP_ENV=production

# Check if Supabase URL and key are set
if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_KEY" ]; then
  echo "Supabase environment variables are set"
else
  echo "WARNING: Supabase environment variables are not set!"
fi

# Give time for any dependent services to be ready
echo "Waiting for dependent services to be ready..."
sleep 5

# Start the application with reduced worker count to avoid memory issues
echo "Starting FastAPI application on port $PORT..."

# Start the application in the background
gunicorn -w 2 -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:$PORT app.main:app \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile - &

# Store the process ID
APP_PID=$!

# Wait for the application to start
echo "Waiting for application to start..."
sleep 10

# Test the health endpoint
echo "Testing health endpoint..."
HEALTH_CHECK=$(curl -s http://localhost:$PORT/api/health || echo "Failed")

if [[ $HEALTH_CHECK == *"healthy"* ]]; then
    echo "Health check successful: $HEALTH_CHECK"
else
    echo "Health check failed: $HEALTH_CHECK"
    # Continue anyway as Railway will handle healthchecks
fi

# Bring the gunicorn process to the foreground
echo "Application ready - bringing process to foreground"
wait $APP_PID 