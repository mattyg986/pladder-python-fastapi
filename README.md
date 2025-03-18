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
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
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

3. Run the unified deployment script:
   ```bash
   ./deploy.sh development
   ```

This will:
- Create a Python virtual environment
- Install all dependencies
- Start the application with hot-reload
- Set up Redis, Celery workers, and all required services

### Production Deployment

For a production-like environment:

```bash
./deploy.sh production
docker-compose up -d
```

### Railway Deployment

To deploy to Railway:

```bash
./deploy.sh railway
```

## 📚 Documentation

For detailed deployment information, see [DEPLOYMENT.md](DEPLOYMENT.md)

## 📊 Services

The application consists of:

1. **Web Service** - FastAPI backend serving the React frontend  
   - URL: http://localhost:8000
   - API Docs: http://localhost:8000/docs

2. **Worker Service** - Celery worker for background tasks

3. **Redis** - Message broker for Celery

## 🧪 Testing

To run tests:

```bash
pytest
```

## 📝 License

This project is licensed under the terms of the license included in the repository.
