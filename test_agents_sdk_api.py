#!/usr/bin/env python3
"""
Test script for the Agents SDK API endpoints.
This script sends requests to the API endpoints to test the Agents SDK functionality.
"""

import os
import json
import asyncio
import logging
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
API_BASE_URL = "http://localhost:8000/api/v1"

def test_process_candidate():
    """Test the process-candidate endpoint."""
    url = f"{API_BASE_URL}/agents-sdk/process-candidate"
    
    # Sample data
    data = {
        "candidate_data": {
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
        },
        "job_data": {
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
    }
    
    # Send the request
    logger.info("Testing process-candidate endpoint...")
    response = requests.post(url, json=data)
    
    # Process the response
    if response.status_code == 200:
        result = response.json()
        logger.info("Request successful!")
        print(f"\nResult: {json.dumps(result, indent=2)}")
        return True
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        print(f"\nError: {response.text}")
        return False

def test_search_candidates():
    """Test the search-candidates endpoint."""
    url = f"{API_BASE_URL}/agents-sdk/search-candidates"
    
    # Sample data
    data = {
        "job_requirements": {
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
    }
    
    # Send the request
    logger.info("Testing search-candidates endpoint...")
    response = requests.post(url, json=data)
    
    # Process the response
    if response.status_code == 200:
        result = response.json()
        logger.info("Request successful!")
        print(f"\nResult: {json.dumps(result, indent=2)}")
        return True
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        print(f"\nError: {response.text}")
        return False

def test_process_task():
    """Test the process-task endpoint."""
    url = f"{API_BASE_URL}/agents-sdk/process-task"
    
    # Sample data
    data = {
        "task_id": "test-task-cultural-fit",
        "action": "evaluate_cultural_fit",
        "parameters": {
            "candidate": {
                "id": "cand123",
                "name": "Jane Smith",
                "skills": ["Python", "Machine Learning", "Data Analysis", "SQL", "TensorFlow"],
                "experience": [
                    {
                        "title": "Data Scientist",
                        "company": "TechCorp",
                        "duration": "3 years"
                    }
                ]
            },
            "company_values": ["Innovation", "Collaboration", "Excellence", "Customer Focus"],
            "team_dynamics": "Fast-paced, autonomous environment with weekly collaborative sessions"
        }
    }
    
    # Send the request
    logger.info("Testing process-task endpoint...")
    response = requests.post(url, json=data)
    
    # Process the response
    if response.status_code == 200:
        result = response.json()
        logger.info("Request successful!")
        print(f"\nResult: {json.dumps(result, indent=2)}")
        return True
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        print(f"\nError: {response.text}")
        return False

def main():
    """Run the tests."""
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is set in environment
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY is not set in the environment. Tests may fail.")
    
    # Run the tests
    print("\n--- Testing Agents SDK API Endpoints ---")
    
    test_process_candidate()
    test_search_candidates()
    test_process_task()
    
    print("\n--- All Tests Completed ---")

if __name__ == "__main__":
    main() 