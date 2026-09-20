import json

class Memory:
    def __init__(self):
        self.file = "memory.json"
        try:
            self.data = json.load(open(self.file))
        except:
            self.data = []

    def save(self, query, response):
        self.data.append({"q": query, "r": response})
        json.dump(self.data, open(self.file, "w"))

    def context(self):
        return self.data[-5:]