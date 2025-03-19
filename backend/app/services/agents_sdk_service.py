import os
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple

from agents import Agent, Runner, function_tool, ModelSettings
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

class CandidateEvaluation(BaseModel):
    """Model for candidate evaluation output."""
    overall_score: int
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendation: str
    justification: str

class AgentSDKService:
    """Service for managing AI agents using OpenAI Agents SDK."""
    
    def __init__(self):
        self.agents = {}
        
    def create_recruiter_agent(self) -> Agent:
        """Create a recruiter agent."""
        if "recruiter" in self.agents:
            return self.agents["recruiter"]
            
        instructions = """
        You are an AI Recruiter specialized in talent acquisition for tech companies.
        
        Your responsibilities include:
        1. Evaluating candidate applications and resumes
        2. Identifying top talent based on job requirements
        3. Providing insights on candidate strengths and weaknesses
        4. Making interview recommendations
        5. Searching for candidates matching specific job requirements
        
        When evaluating candidates:
        - Focus on both technical skills and cultural fit
        - Consider experience, education, and portfolio
        - Identify specific strengths that match job requirements
        - Highlight areas for growth or potential concerns
        - Provide a clear recommendation (Interview, Consider, or Reject)
        
        When searching for candidates:
        - Match technical skills to job requirements
        - Consider experience level and seniority needs
        - Look for relevant industry experience
        - Calculate a match score based on alignment with requirements
        
        Always provide specific, data-driven recommendations and insights.
        """
        
        agent = Agent(
            name="AI Recruiter",
            instructions=instructions,
            model="gpt-4o",
            model_settings=ModelSettings(
                temperature=0.2
            )
        )
        
        self.agents["recruiter"] = agent
        return agent
    
    def create_processor_agent(self) -> Agent:
        """Create an application processor agent."""
        if "processor" in self.agents:
            return self.agents["processor"]
            
        instructions = """
        You are an AI Application Processor specialized in screening and processing job applications.
        
        Your responsibilities include:
        1. Extracting structured information from resumes and applications
        2. Tagging and categorizing applications based on skills and experience
        3. Identifying missing information in applications
        4. Providing preliminary evaluations
        5. Ranking applications for further review
        
        When processing applications:
        - Extract key information (skills, experience, education, etc.)
        - Flag applications that match specific requirements
        - Identify discrepancies or missing information
        - Prioritize applications based on matching criteria
        
        Always focus on objective evaluation and data extraction.
        Avoid making biased judgments based on non-relevant factors.
        """
        
        agent = Agent(
            name="AI Application Processor",
            instructions=instructions,
            model="gpt-4o",
            model_settings=ModelSettings(
                temperature=0.1
            )
        )
        
        self.agents["processor"] = agent
        return agent
    
    def create_matcher_agent(self) -> Agent:
        """Create a job matcher agent."""
        if "matcher" in self.agents:
            return self.agents["matcher"]
            
        instructions = """
        You are an AI Job Matcher specialized in matching candidates to job opportunities.
        
        Your responsibilities include:
        1. Analyzing job descriptions to extract key requirements
        2. Evaluating candidate profiles against job requirements
        3. Calculating match scores and compatibility ratings
        4. Generating personalized recommendations
        5. Explaining match rationale
        
        When matching candidates to jobs:
        - Consider both technical skills and soft skills
        - Evaluate experience level appropriately
        - Account for transferable skills from other domains
        - Consider career trajectory and growth potential
        - Provide a match percentage and detailed reasoning
        
        Focus on finding the right matches for long-term success, not just immediate needs.
        """
        
        agent = Agent(
            name="AI Job Matcher",
            instructions=instructions,
            model="gpt-4o",
            model_settings=ModelSettings(
                temperature=0.3
            )
        )
        
        self.agents["matcher"] = agent
        return agent
    
    def create_search_agent(self) -> Agent:
        """Create a search agent."""
        if "search" in self.agents:
            return self.agents["search"]
            
        instructions = """
        You are an AI Search Agent specialized in finding and filtering candidates and jobs.
        
        Your responsibilities include:
        1. Processing complex search queries
        2. Finding candidates based on specific criteria
        3. Searching for jobs matching candidate profiles
        4. Refining search results based on feedback
        5. Explaining search rationale
        
        When performing searches:
        - Interpret natural language search queries accurately
        - Consider synonyms and related terms
        - Apply appropriate filters and ranking
        - Provide diverse but relevant results
        - Explain why each result was included
        
        Ensure your search results are comprehensive but focused on quality matches.
        """
        
        agent = Agent(
            name="AI Search Agent",
            instructions=instructions,
            model="gpt-4o",
            model_settings=ModelSettings(
                temperature=0.2
            )
        )
        
        self.agents["search"] = agent
        return agent
    
    def create_triage_agent(self) -> Agent:
        """Create a triage agent to route to specialized agents."""
        if "triage" in self.agents:
            return self.agents["triage"]
            
        # Create all specialized agents first
        recruiter = self.create_recruiter_agent()
        processor = self.create_processor_agent()
        matcher = self.create_matcher_agent()
        search = self.create_search_agent()
        
        instructions = """
        You are a triage agent for a talent platform. Your job is to:
        
        1. Analyze the input task and determine which specialized agent should handle it
        2. Route the task to the appropriate specialized agent
        
        Available agents:
        - Recruiter: For evaluating candidates and providing hiring recommendations
        - Processor: For extracting and processing application information
        - Matcher: For matching candidates to job opportunities
        - Search: For finding candidates based on specific criteria
        
        Make your decision based on the nature of the task and required expertise.
        """
        
        triage = Agent(
            name="Triage Agent",
            instructions=instructions,
            handoffs=[recruiter, processor, matcher, search],
            model="gpt-4o",
            model_settings=ModelSettings(
                temperature=0.0  # Low temperature for more deterministic routing
            )
        )
        
        self.agents["triage"] = triage
        return triage
    
    @function_tool
    def get_candidate_history(self, candidate_id: str) -> Dict[str, Any]:
        """Retrieve candidate application history."""
        # Mock implementation - would connect to database in production
        return {
            "previous_applications": [
                {"job_id": "job123", "status": "Rejected", "date": "2023-01-15"},
                {"job_id": "job456", "status": "Interviewed", "date": "2023-03-22"}
            ],
            "interviews": [
                {"job_id": "job456", "score": 7, "feedback": "Good technical skills, needs improvement in communication"}
            ]
        }
    
    async def process_candidate(self, candidate_data: Dict[str, Any], job_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a candidate using the recruiter agent."""
        recruiter = self.create_recruiter_agent()
        
        # Format the query with candidate and job data
        query = f"Analyze this candidate: {candidate_data}"
        if job_data:
            query += f"\n\nFor this job: {job_data}"
        
        query += """
        Provide:
        1. Overall assessment (score out of 100)
        2. Key strengths (at least 3)
        3. Areas for improvement (at least 2)
        4. Recommendation (Interview, Consider, or Reject)
        5. Justification for your recommendation
        
        Format your response in a clear, structured way.
        """
        
        # Run the agent
        result = await Runner.run(recruiter, input=query)
        return {
            "assessment": result.final_output,
            "candidate_id": candidate_data.get("id"),
            "name": candidate_data.get("name")
        }
    
    async def search_candidates(self, job_requirements: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for candidates matching job requirements."""
        search = self.create_search_agent()
        
        # Format the query
        query = f"Find candidates matching these job requirements: {job_requirements}"
        if filters:
            query += f"\n\nApply these filters: {filters}"
        
        query += """
        For each matching candidate, provide:
        1. Match score (0-100)
        2. Key matching skills and qualifications
        3. Potential fit assessment
        
        Return the top 5 candidates ordered by match score.
        """
        
        # Run the agent
        result = await Runner.run(search, input=query)
        return {
            "search_results": result.final_output,
            "job_id": job_requirements.get("job_id"),
            "title": job_requirements.get("title")
        }
    
    async def process_task(self, task_id: str, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task using the appropriate agent."""
        # Create a Triage agent to route to the appropriate specialized agent
        triage = self.create_triage_agent()
        
        # Format the query
        query = f"Task ID: {task_id}\nAction: {action}\nParameters: {parameters}\n\nProcess this task according to the action type."
        
        # Run the agent
        result = await Runner.run(triage, input=query)
        
        return {
            "task_id": task_id,
            "action": action,
            "result": result.final_output,
            "status": "completed"
        } 