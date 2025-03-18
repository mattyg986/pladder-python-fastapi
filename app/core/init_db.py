import logging
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.models.agent import Agent, AgentTaskModel
from app.schemas.agent import AgentType, AgentStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize the database."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")


def create_initial_data() -> None:
    """Create initial data in the database."""
    db = next(get_db())
    
    # Check if we already have agents
    existing_agents = db.query(Agent).count()
    if existing_agents > 0:
        logger.info("Database already contains data. Skipping initial data creation.")
        return
    
    # Create sample agents
    sample_agents = [
        Agent(
            name="Recruiter Agent",
            type=AgentType.RECRUITER,
            description="AI agent for candidate sourcing and evaluation",
            status=AgentStatus.ACTIVE,
            parameters={
                "matching_threshold": 0.7,
                "max_candidates": 10
            }
        ),
        Agent(
            name="Application Processor",
            type=AgentType.PROCESSOR,
            description="AI agent for processing job applications",
            status=AgentStatus.ACTIVE,
            parameters={
                "auto_reject_threshold": 0.3,
                "auto_advance_threshold": 0.8
            }
        ),
        Agent(
            name="Job Matcher",
            type=AgentType.MATCHER,
            description="AI agent for matching candidates to jobs",
            status=AgentStatus.ACTIVE,
            parameters={
                "similarity_algorithm": "cosine",
                "minimum_score": 0.6
            }
        )
    ]
    
    db.add_all(sample_agents)
    db.commit()
    
    logger.info(f"Created {len(sample_agents)} sample agents")


if __name__ == "__main__":
    logger.info("Creating database tables")
    init_db()
    logger.info("Creating initial data")
    create_initial_data()
    logger.info("Initial data created") 