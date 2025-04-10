# AI Telegram Agent

A Telegram bot using local Ollama model for processing user queries based on a knowledge base.

## Features

- 🤖 Local LLM model integration via Ollama
- 💬 Telegram integration
- 📚 Vector database for knowledge storage and retrieval
- 🔍 Semantic search for relevant information
- 🧠 Contextual memory for dialogue support

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) with llama2 model installed
- Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/valkorostyslav/ai_telegram_agent.git
cd ai_telegram_agent
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
# or
.\venv\Scripts\activate  # for Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy .env.example to .env and configure environment variables:
```bash
cp .env.example .env
```

5. Start Ollama server and ensure llama2 model is installed:
```bash
ollama run llama2
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. Open Telegram and start chatting with the bot

## Project Structure

- `main.py` - main bot entry point
- `agent/` - core bot logic
  - `chatbot.py` - message processing and LLM interaction
  - `knowledge_base.py` - vector database operations
- `data/` - knowledge base files
- `chroma_db/` - directory for vector database storage 