#!/usr/bin/env python3
"""
Test script for OpenAI Assistant integration.
This script initializes the OpenAI Assistant and runs a sample task.
"""

import os
import json
import logging
from dotenv import load_dotenv

from app.services.openai_service import OpenAIAssistantService
from app.core.init_assistants import init_recruiter_assistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the test."""
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY is not set in the .env file")
        print("\nPlease set your OpenAI API key in the .env file and try again.")
        return
    
    # Initialize the OpenAI service
    openai_service = OpenAIAssistantService()
    
    # Initialize the recruiter assistant
    assistant_id = init_recruiter_assistant(openai_service)
    logger.info(f"Using recruiter assistant: {assistant_id}")
    
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
    
    # Run a sample task
    print("\n--- Testing candidate evaluation ---")
    task_id = "test-task-001"
    result = openai_service.process_task(
        task_id=task_id,
        assistant_id=assistant_id,
        task_data={
            "action": "process_candidate",
            "candidate_data": sample_candidate,
            "job_data": sample_job,
            "instructions": """
            Evaluate this candidate for the Senior Data Scientist position.
            
            Provide:
            1. Overall fit score (0-100)
            2. Analysis of strengths and weaknesses
            3. Whether they meet the minimum requirements
            4. Recommendation (Interview, Consider, or Reject)
            
            Format your response in a clear, structured way.
            """
        }
    )
    
    print("\n--- Result ---")
    if result.get("status") == "completed":
        for i, message in enumerate(result.get("messages", [])):
            print(f"\nResponse {i+1}:\n{message}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("\n--- Test Complete ---")

if __name__ == "__main__":
    main() 