from agents.research_agent import ResearchAgent
from agents.retrieval_agent import RetrievalAgent
from agents.sql_agent import SQLAgent
from agents.report_agent import ReportAgent
from agents.validation_agent import ValidationAgent
from core.memory import Memory

class Manager:
    def __init__(self):
        self.research = ResearchAgent()
        self.retrieval = RetrievalAgent()
        self.sql = SQLAgent()
        self.report = ReportAgent()
        self.validator = ValidationAgent()
        self.memory = Memory()

    def handle(self, query, role):
        # Get previous context from memory
        context = self.memory.context()
        
        # Construct query with context if available
        if context:
            context_str = "\n".join([f"Q: {c['q']}\nA: {c['r']}" for c in context])
            full_query = f"Previous conversation:\n{context_str}\n\nCurrent question: {query}"
        else:
            full_query = query
        
        # Route to appropriate agent based on query type
        if "database" in query.lower() or "sql" in query.lower():
            data = self.sql.run(full_query)
        elif "research" in query.lower() or "analyze" in query.lower():
            data = self.research.run(full_query)
        else:
            data = self.retrieval.run(full_query)

        # Generate report based on role
        report = self.report.generate(data, role)

        # Validate the report
        if not self.validator.validate(report):
            # Save failed attempt to memory
            self.memory.save(query, "Validation failed")
            return "Validation failed - Please try again"

        # Save successful response to memory
        self.memory.save(query, report)

        return report
