import os
from operator import itemgetter
from typing import Callable, List, Optional

from langchain_core.messages import BaseMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr


def get_chatbot() -> Callable[..., str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key is None:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("MAX_TOKENS", "512"))

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=SecretStr(api_key),
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """Ви - віртуальний консультант автосалону AutoDream. Ваша роль - допомагати клієнтам з питаннями про автомобілі та послуги салону.

                Важливі правила:
                    1. Відповідайте ТІЛЬКИ на основі наданої інформації про автосалон
                    2. Якщо в контексті є інформація про автомобілі - ОБОВ'ЯЗКОВО надайте її користувачу
                    3. При запиті про доступні моделі - ОБОВ'ЯЗКОВО перерахуйте всі моделі з розділу "Автомобілі в наявності"
                    4. Якщо знайдено інформацію про автомобілі - вкажіть всі деталі: модель, двигун, пробіг, ціну, колір, комплектацію
                    5. При запиті контактів - надайте ВСЮ контактну інформацію: адресу, телефон, графік роботи, сайт, соцмережі
                    6. Якщо питання не стосується автомобілів, послуг салону або виходить за межі вашої бази знань, ввічливо поясніть:
                        - Що ви консультант AutoDream
                        - Що можете відповідати лише на питання про автомобілі та послуги салону
                        - Запропонуйте задати питання про доступні авто, умови придбання, тест-драйв чи сервіс

                Контекст з бази знань:
                {context}

                Запитання користувача: {question}"""
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    def get_context() -> str:
        try:
            with open("data/knowledge.txt", "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading knowledge base: {e}")
            return "На жаль, виникла помилка при читанні бази знань. Спробуйте, будь ласка, пізніше."

    chain = (
        {
            "context": lambda x: get_context(),
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
