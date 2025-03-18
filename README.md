# Purple Ladder AI Agents Platform

A Python microservice for the Purple Ladder talent/job platform that manages AI Recruiters and other specialized agents for application processing, searching, matching, and more.

## 🏗️ Architecture

- **Backend**: FastAPI + Python
- **AI Framework**: OpenAI Agents SDK
- **Task Management**: Celery
- **Task Monitoring**: Flower (UI for Celery)
- **Frontend**: React

## 🤖 Core Features

- AI Recruiter Agents
- Application Processing Agents
- Search Agents
- Candidate-Job Matching Agents
- Agent Orchestration
- Real-time Task Monitoring

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Redis (for Celery broker)
- Node.js 18+ and npm (for React frontend)
- OpenAI API Key

### Local Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/pladder-python-fastapi.git
   cd pladder-python-fastapi
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Run the start script (this will set up everything automatically):
   ```bash
   ./start.sh
   ```

The script will:
- Create a Python virtual environment (if it doesn't exist)
- Install all dependencies
- Start Redis
- Start the Celery worker
- Start the FastAPI backend
- Start the React frontend

### Manual Setup

If you prefer to set up each component manually:

1. Set up Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up frontend:
   ```bash
   cd frontend
   npm install
   ```

3. Start Redis:
   ```bash
   redis-server  # Or: brew services start redis
   ```

4. Start Celery worker:
   ```bash
   celery -A app.worker worker --loglevel=info
   ```

5. Start the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Start the React frontend:
   ```bash
   cd frontend
   npm start
   ```

## 🌐 Deployment to Railway

This application is ready for deployment to Railway:

1. Fork this repository

2. Create a new project on [Railway](https://railway.app/)

3. Connect your repository to Railway

4. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `RAILWAY_ENVIRONMENT`: Set to `production`
   - `SECRET_KEY`: Generate a random secret key for security

5. Add a Redis service to your project
   - Railway will automatically inject the `REDIS_URL` environment variable

6. (Optional) Add a PostgreSQL service if you need a database
   - Railway will automatically inject the `DATABASE_URL` environment variable

7. Deploy!

Railway will automatically:
- Install dependencies (Python and Node.js)
- Build the frontend
- Deploy the full stack application

### Environment Variables

The application uses the following environment variables:

| Variable | Description | Default (Development) | Railway (Production) |
|----------|-------------|----------------------|---------------------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Must be set manually |
| `RAILWAY_ENVIRONMENT` | Environment type | `development` | `production` |
| `DATABASE_URL` | Database connection string | `sqlite:///./app.db` | Auto-provided with PostgreSQL |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` | Auto-provided with Redis |
| `SECRET_KEY` | Secret key for security | Generated locally | Auto-generated |
| `FRONTEND_URL` | URL of the frontend | `http://localhost:3000` | Your Railway URL |
| `PORT` | Port to run the server | `8000` | Auto-provided |

For local development, copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with your values
```

## 🐳 Docker Deployment

The application is configured for deployment using Docker, which is recommended for production environments:

### Local Docker Development

1. Make sure Docker and Docker Compose are installed on your system
2. Clone the repository
3. Create a `.env` file with your OpenAI API key
4. Run with Docker Compose:
   ```bash
   docker-compose up
   ```
5. Access the application at http://localhost:8000

### Railway Deployment with Docker

1. Fork this repository
2. Create a new project on [Railway](https://railway.app/)
3. Connect your repository
4. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SECRET_KEY`: A secure random string for encryption
5. Add a Redis service to your project
6. Deploy!

Railway will:
1. Detect the Dockerfile and build it
2. Start the container with your environment variables
3. Expose the service on a public URL

### Why Docker?

Docker provides several advantages for deploying this application:
- Consistent environment across development and production
- Proper isolation of dependencies
- Easy scaling
- Simplified deployment process

## 📁 Project Structure

```
pladder-python-fastapi/
├── app/                    # Backend application
│   ├── api/                # API endpoints
│   │   ├── v1/             # API version 1
│   ├── agents/             # AI agent implementations
│   │   ├── celery_tasks.py # Unified Celery tasks
│   ├── core/               # Core application components
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic services
│   │   ├── agents_sdk_service.py # OpenAI Agents SDK service
│   ├── static/             # Static files (built frontend)
│   ├── worker.py           # Celery worker configuration
│   └── main.py             # FastAPI application entry point
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   └── package.json
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── app.json                # Railway application metadata
├── railway.json            # Railway configuration
├── start.sh                # Local development startup script
├── stop.sh                 # Stop all services
├── build.sh                # Production build script
└── README.md               # This file
```

## 🔧 Development

- API documentation available at `/docs` when running the application
- Access the frontend at `http://localhost:3000` during development
- Access the API at `http://localhost:8000` during development

## 📄 License

This project is licensed under the terms of the license included in the repository.
