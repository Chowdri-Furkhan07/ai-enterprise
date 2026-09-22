class ReportAgent:
    def generate(self, data, role):
        if role == "admin":
            return f"Detailed Report: {data}"
        elif role == "analyst":
            return f"Analysis: {data}"
        else:
            return f"Summary: {data}"
