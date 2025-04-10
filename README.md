# AI Telegram Agent

A Telegram bot consultant for a car dealership based on Google Gemini API with conversation context support and knowledge base.

## Features

- 🤖 Google Gemini API integration for query processing
- 💬 Telegram integration
- 📚 Knowledge base storage and file reading
- 🧠 Conversation context support (last 10 messages)
- 🔄 Automatic knowledge base updates (reading before each response)
- 🎯 Specialization in car dealership consulting

## Requirements

- Python 3.8+
- Gemini API Key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
- Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

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

4. Create .env file based on .env.example:
```bash
cp .env.example .env
```

5. Configure environment variables in .env:
- Add your Telegram Bot Token (TELEGRAM_BOT_TOKEN)
- Add your Gemini API Key (GEMINI_API_KEY)
- Optionally configure TEMPERATURE and MAX_TOKENS

## Usage

1. Start the bot:
```bash
python main.py
```

2. Open Telegram and start chatting with the bot

## Project Structure

- `main.py` - main bot file
- `agent/` - core bot logic
  - `chatbot.py` - message processing and Gemini API interaction
- `data/` - knowledge base files
  - `knowledge.txt` - dealership knowledge base
- `.env` - configuration variables

## Functionality

1. **Telegram Communication**
   - Instant message responses
   - User-friendly Telegram interface
   - /start command to begin interaction

2. **Context Support**
   - Conversation history storage for each user
   - Limited to last 10 messages
   - Context utilization for response generation

3. **Knowledge Base**
   - Information storage in text file
   - Updates without bot restart
   - Automatic reading before each response

4. **Consulting**
   - Available cars information
   - Purchase and financing conditions
   - Test drive scheduling
   - Warranty and service
   - Contact information

## Security

- API keys stored in .env file
- Conversation history stored only in memory
- Limited number of messages in history

## Development

To modify the knowledge base, simply edit the `data/knowledge.txt` file. Changes will be applied automatically on the next query to the bot.

## License

MIT 