from core.llm import LLM

class ResearchAgent:
    def __init__(self):
        self.llm = LLM()

    def run(self, topic):
        prompt = f"""
        You are a research expert.
        Provide detailed insights, trends, and analysis on:
        {topic}
        """
        return self.llm.generate(prompt)
