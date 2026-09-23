from crewai import Task

def create_tasks(research_agent, retrieval_agent, report_agent):
    task1 = Task(
        description="Retrieve relevant documents from vector DB",
        agent=retrieval_agent,
        expected_output="Relevant document chunks"
    )

    task2 = Task(
        description="Perform deep research analysis",
        agent=research_agent,
        expected_output="Insights and analysis"
    )

    task3 = Task(
        description="Generate final structured report",
        agent=report_agent,
        expected_output="Final report"
    )

    return [task1, task2, task3]
