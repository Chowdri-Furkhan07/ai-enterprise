from langchain.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader

def load_file(path):
    if path.endswith(".pdf"):
        return PyPDFLoader(path).load()
    elif path.endswith(".csv"):
        return CSVLoader(path).load()
    elif path.endswith(".docx"):
        return Docx2txtLoader(path).load()