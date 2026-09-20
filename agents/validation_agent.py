class ValidationAgent:
    def validate(self, res):
        return "error" not in res.lower()