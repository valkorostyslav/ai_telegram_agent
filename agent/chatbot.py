from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI

CHROMA_PATH = "chroma_db"


def get_chatbot():
    # Використання OpenAI з локальним Ollama
    llm = ChatOpenAI(
        model="llama3.2",
        temperature=0.7,
        max_tokens=512,
        openai_api_key="ollama",
        openai_api_base="http://localhost:11434/v1",
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

    # Створюємо ланцюжок з пам'яттю
    memory = ConversationBufferWindowMemory(
        k=5,
        return_messages=True,
        memory_key="history",
        input_key="question",  # Вказуємо ключ для вхідного повідомлення
    )

    conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

    # Функція для обробки запитів
    def process_query(query):
        # Отримуємо релевантні документи
        docs = retriever.get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in docs])

        # Отримуємо відповідь
        response = conversation.predict(
            question=query, context=context
        )  # Змінили input на question
        return response

    return process_query
