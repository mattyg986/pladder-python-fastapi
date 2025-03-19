FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json .npmrc ./

# Install dependencies
RUN npm install --production --no-optional --prefer-offline

# Copy the rest of the application
COPY public ./public
COPY src ./src
COPY *.js ./

# Build the application
ARG REACT_APP_SUPABASE_URL
ARG REACT_APP_SUPABASE_ANON_KEY
ARG REACT_APP_API_URL

ENV REACT_APP_SUPABASE_URL=${REACT_APP_SUPABASE_URL}
ENV REACT_APP_SUPABASE_ANON_KEY=${REACT_APP_SUPABASE_ANON_KEY}
ENV REACT_APP_API_URL=${REACT_APP_API_URL:-http://localhost:8000}

# Hard-code Supabase URLs for local development when not set
ENV REACT_APP_SUPABASE_URL=${REACT_APP_SUPABASE_URL:-https://dyfnqcybcnvuhxreflqu.supabase.co}
ENV REACT_APP_SUPABASE_ANON_KEY=${REACT_APP_SUPABASE_ANON_KEY:-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5Zm5xY3liY252dWh4cmVmbHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk5MzM4MzYsImV4cCI6MjA1NTUwOTgzNn0.eq0vCqZXghv1U-ANCuGGJWi6LYTuxxEqhdtEgPY_PSE}

# Build the React app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy the build files from the builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 