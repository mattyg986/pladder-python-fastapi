# Purple Ladder AI Agents Platform

A Python microservice for the Purple Ladder talent/job platform that manages AI Recruiters and other specialized agents for application processing, searching, matching, and more.

## 🏗️ Architecture

- **Backend**: FastAPI + Python
- **Task Management**: Celery
- **Task Monitoring**: Flower (UI for Celery)
- **AI Framework**: Agents SDK Python
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

- Python 3.10+
- Redis (for Celery broker)
- Node.js and npm (for React frontend)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/pladder-python-fastapi.git
   cd pladder-python-fastapi
   ```

2. Set up Python environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up frontend
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. Start the Redis server (for Celery)
   ```bash
   redis-server
   ```

2. Start Celery worker
   ```bash
   celery -A app.worker worker --loglevel=info
   ```

3. Start Flower (Celery monitoring)
   ```bash
   celery -A app.worker flower --port=5555
   ```

4. Start the FastAPI backend
   ```bash
   uvicorn app.main:app --reload
   ```

5. Start the React frontend
   ```bash
   cd frontend
   npm start
   ```

## 📁 Project Structure

```
pladder-python-fastapi/
├── app/                    # Backend application
│   ├── api/                # API endpoints
│   │   ├── recruiter/      # Recruiter agent logic
│   │   ├── processor/      # Application processor agent
│   │   ├── matcher/        # Job matching agent
│   │   └── search/         # Search agent
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic services
│   ├── worker.py           # Celery worker configuration
│   └── main.py             # FastAPI application entry point
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🔧 Development

- API documentation available at `/docs` when running the application
- Flower dashboard available at `http://localhost:5555`

## 📄 License

This project is licensed under the terms of the license included in the repository.
