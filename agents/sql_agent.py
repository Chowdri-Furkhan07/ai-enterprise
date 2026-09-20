from database.mysql import run_query

class SQLAgent:
    def run(self, q):
        return run_query(q)