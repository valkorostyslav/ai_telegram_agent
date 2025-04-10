from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

CHROMA_PATH = "chroma_db"


def load_knowledge_base():
    # Читаємо знання з файлу
    with open("data/knowledge.txt", "r", encoding="utf-8") as f:
        texts = f.read().split("\n\n")

    # Векторизація
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Створення векторної бази
    db = Chroma.from_texts(texts, embedding_function, persist_directory=CHROMA_PATH)

    return db
