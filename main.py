import os
from typing import Dict, List

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from agent.chatbot import get_chatbot
from agent.knowledge_base import load_knowledge_base

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

print("📥 Індексуємо знання...")
load_knowledge_base()

print("🧠 Завантажуємо чатбота...")
process_query = get_chatbot()

# Dictionary to store conversation history for each user
conversation_history: Dict[int, List] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = """👋 Вітаю! Я консультант автосалону AutoDream.

🚗 Я допоможу вам:
- Підібрати автомобіль
- Розповісти про наявні моделі
- Пояснити умови придбання
- Записати на тест-драйв
- Відповісти на питання про гарантію та сервіс

Просто напишіть ваше питання, і я з радістю допоможу! 🤝"""
    await update.message.reply_text(welcome_message)
    conversation_history[update.effective_user.id] = []


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_input = update.message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    history = conversation_history[user_id]

    response = process_query(user_input, history)

    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))

    conversation_history[user_id] = history[-10:]

    await update.message.reply_text(response)


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот працює. Очікує повідомлення...")
    app.run_polling()


if __name__ == "__main__":
    main()
