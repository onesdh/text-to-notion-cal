import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG_MS = {
    "host": os.getenv("DB_HOST_MS"),
    "port": int(os.getenv("DB_PORT_MS", 3306)),
    "user": os.getenv("DB_USER_MS"),
    "password": os.getenv("DB_PASSWORD_MS"),
    "database": os.getenv("DB_DATABASE_MS"),
}

GRAPH_DB_CONFIG_NEO4J = {
    "url": os.getenv("NEO4J_URL"),
    "username": os.getenv("NEO4J_USERNAME"),
    "password": os.getenv("NEO4J_PASSWORD"),
}

GPT_API_KEY = os.getenv("GPT_API_KEY")
GPT_LLM_MODEL = os.getenv("GPT_LLM_MODEL", "gpt-4o-mini")

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "bge-m3")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "llama3.1:8b")

QDRANT_URL = os.getenv("QDRANT_URL")


NOTION_TOKEN = os.getenv("NOTION_TOKEN")  # Notion 통합 토큰
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")  # 데이터베이스 ID

TEMPERATURE = 0.7
TOP_P = 0.9
