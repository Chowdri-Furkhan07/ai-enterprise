from crewai import Agent, Crew, Task, Process
from core.llm import LLM
from core.pinecone_db import PineconeStore

class EnterpriseCrew:
    def __init__(self):
        self.llm = LLM()
        self.vector_store = PineconeStore()
        
        # Create agents
        self.researcher = Agent(
            role="Research Analyst",
            goal="Research and analyze data to provide comprehensive insights",
            backstory="""
            You are an expert research analyst with deep knowledge in data analysis,
            market research, and trend identification. You provide detailed and accurate insights.
            """,
            verbose=True,
            llm=self.llm
        )
        
        self.retriever = Agent(
            role="Document Retriever",
            goal="Fetch and retrieve relevant documents from the knowledge base",
            backstory="""
            You are a document retrieval specialist with access to the enterprise
            knowledge base. You find the most relevant documents for any query.
            """,
            verbose=True,
            llm=self.llm
        )
        
        self.reporter = Agent(
            role="Report Generator",
            goal="Create comprehensive reports based on research and retrieved data",
            backstory="""
            You are an expert report writer. You create well-structured, detailed reports
            tailored to different roles (admin, analyst, viewer).
            """,
            verbose=True,
            llm=self.llm
        )
        
        self.validator = Agent(
            role="Data Validator",
            goal="Validate research findings and ensure accuracy",
            backstory="""
            You are a data validation expert. You ensure all research findings are
            accurate, consistent, and meet quality standards.
            """,
            verbose=True,
            llm=self.llm
        )
    
    def create_crew(self, query, role="analyst"):
        # Create tasks
        research_task = Task(
            description=f"Research and provide detailed insights on: {query}",
            agent=self.researcher,
            expected_output="Comprehensive research findings and insights"
        )
        
        retrieval_task = Task(
            description=f"Retrieve relevant documents for: {query}",
            agent=self.retriever,
            expected_output="Relevant documents and data from the knowledge base"
        )
        
        report_task = Task(
            description=f"Generate a {role} report based on research and documents",
            agent=self.reporter,
            expected_output=f"A well-structured {role} report"
        )
        
        validation_task = Task(
            description=f"Validate the research findings for accuracy",
            agent=self.validator,
            expected_output="Validation report confirming accuracy"
        )
        
        # Create crew with sequential process
        crew = Crew(
            agents=[self.researcher, self.retriever, self.reporter, self.validator],
            tasks=[research_task, retrieval_task, report_task, validation_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew
    
    def run(self, query, role="analyst"):
        """Run the crew with a query"""
        crew = self.create_crew(query, role)
        result = crew.kickoff()
        return result


# Singleton instance
crew = EnterpriseCrew()

