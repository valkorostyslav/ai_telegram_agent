from operator import itemgetter
from typing import Any, Callable, Dict, List, Optional

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.messages import BaseMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

CHROMA_PATH = "chroma_db"


def get_chatbot() -> Callable[..., str]:
    llm = ChatOpenAI(
        model="llama3.2",
        temperature=0.7,
        max_tokens=512,
        api_key="ollama",
        base_url="http://localhost:11434/v1",
    )

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_function
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """Ви - віртуальний консультант автосалону AutoDream. Ваша роль - допомагати клієнтам з питаннями про автомобілі та послуги салону.

                Важливі правила:
                    1. Відповідайте ТІЛЬКИ на основі наданої інформації про автосалон
                    2. Якщо питання не стосується автомобілів, послуг салону або виходить за межі вашої бази знань, ввічливо поясніть:
                        - Що ви консультант AutoDream
                        - Що можете відповідати лише на питання про автомобілі та послуги салону
                        - Запропонуйте задати питання про доступні авто, умови придбання, тест-драйв чи сервіс

Контекст з бази знань: {context}
Запитання користувача: {question}"""
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    def get_context(input_dict: Dict[str, Any]) -> str:
        docs = retriever.invoke(input_dict["question"])
        return "\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": lambda x: get_context(x),
            "question": itemgetter("question"),
            "history": lambda x: x.get("history", []),
        }
        | prompt
        | llm
    )

    def process_query(query: str, history: Optional[List[BaseMessage]] = None) -> str:
        if history is None:
            history = []
        response = chain.invoke({"question": query, "history": history})
        return str(response.content)

    return process_query
