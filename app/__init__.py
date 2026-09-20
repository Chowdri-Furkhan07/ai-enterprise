"""
Enterprise AI Assistant Application
"""

__version__ = "1.0.0"

from app.main import app
from app.config import (
    AWS_REGION,
    MODEL_ID,
    PINECONE_API_KEY,
    MYSQL_CONFIG
)
