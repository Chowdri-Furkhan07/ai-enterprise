from core.llm import LLM
from database.mysql import run_query

class SQLTool:
    def __init__(self):
        self.llm = LLM()

    def nl_to_sql(self, question):
        prompt = f"""
        Convert the following natural language question into SQL:
        Question: {question}
        Only return SQL query.
        """
        return self.llm.generate(prompt)

    def execute(self, question):
        sql = self.nl_to_sql(question)
        try:
            result = run_query(sql)
            return {"sql": sql, "result": result}
        except Exception as e:
            return {"error": str(e), "sql": sql}