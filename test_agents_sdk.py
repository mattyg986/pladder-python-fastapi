#!/usr/bin/env python3
"""
Test script for OpenAI Agents SDK integration.
This script tests the Agent SDK service with sample tasks.
"""

import os
import json
import logging
import asyncio
from dotenv import load_dotenv

from app.services.agents_sdk_service import AgentSDKService
from agents import set_tracing_disabled

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Run the tests."""
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY is not set in the .env file")
        print("\nPlease set your OpenAI API key in the .env file and try again.")
        return
    
    # Enable tracing by default (set_tracing_disabled(False) enables tracing)
    set_tracing_disabled(False)
    
    # Initialize the Agent SDK service
    agent_service = AgentSDKService()
    
    # Create a sample candidate
    sample_candidate = {
        "id": "cand123",
        "name": "Jane Smith",
        "skills": ["Python", "Machine Learning", "Data Analysis", "SQL", "TensorFlow"],
        "experience": [
            {
                "title": "Data Scientist",
                "company": "TechCorp",
                "duration": "3 years",
                "description": "Developed ML models for customer segmentation and churn prediction."
            },
            {
                "title": "ML Engineer",
                "company": "AI Solutions Inc.",
                "duration": "2 years",
                "description": "Built and deployed NLP models for sentiment analysis and text classification."
            }
        ],
        "education": [
            {
                "degree": "Master's in Computer Science",
                "institution": "Stanford University",
                "year": 2018
            }
        ]
    }
    
    # Create a sample job requirement
    sample_job = {
        "job_id": "job456",
        "title": "Senior Data Scientist",
        "requirements": [
            "5+ years of experience in Data Science or Machine Learning",
            "Proficiency in Python and SQL",
            "Experience with deep learning frameworks (TensorFlow or PyTorch)",
            "Strong problem-solving and analytical skills",
            "Experience leading data science projects"
        ],
        "preferred": [
            "PhD in Computer Science, Statistics, or related field",
            "Experience in cloud computing platforms (AWS, GCP)",
            "Publications in ML conferences"
        ]
    }
    
    # Test 1: Process a candidate
    print("\n--- Test 1: Processing Candidate with Recruiter Agent ---")
    result = await agent_service.process_candidate(sample_candidate, sample_job)
    print(f"\nResult: {json.dumps(result, indent=2)}")
    
    # Test 2: Search for candidates
    print("\n--- Test 2: Searching Candidates with Search Agent ---")
    result = await agent_service.search_candidates(sample_job)
    print(f"\nResult: {json.dumps(result, indent=2)}")
    
    # Test 3: Using the triage agent
    print("\n--- Test 3: Using Triage Agent ---")
    result = await agent_service.process_task(
        task_id="test-task-003",
        action="evaluate_cultural_fit",
        parameters={
            "candidate": sample_candidate,
            "company_values": ["Innovation", "Collaboration", "Excellence", "Customer Focus"],
            "team_dynamics": "Fast-paced, autonomous environment with weekly collaborative sessions"
        }
    )
    print(f"\nResult: {json.dumps(result, indent=2)}")
    
    print("\n--- All Tests Completed ---")

if __name__ == "__main__":
    asyncio.run(main()) 