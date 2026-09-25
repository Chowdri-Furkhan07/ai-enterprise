import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB")
}

JWT_SECRET = os.getenv("JWT_SECRET")
