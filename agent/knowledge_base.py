import os

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

CHROMA_PATH = "chroma_db"

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def load_knowledge_base():
    with open("data/knowledge.txt", "r", encoding="utf-8") as f:
        texts = f.read().split("\n\n")

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    db = Chroma.from_texts(texts, embedding_function, persist_directory=CHROMA_PATH)

    return db
