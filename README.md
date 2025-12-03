# Telegram Bot with LangChain & DeepSeek

AI-powered Telegram bot using LangChain framework and DeepSeek for intelligent responses.

## 🚀 Quick Start

1. **Clone & Setup**
   ```bash
   git clone https://github.com/yourusername/python_telegram_bot_langchain_1.git
   cd python_telegram_bot_langchain_1
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   Create `.env` file:
   ```env
   YOUR_TELEGRAM_BOT_TOKEN=your_bot_token
   DEEPSEEK_API_KEY=your_deepseek_key
   ```

3. **Run Bot**
   ```bash
   python bot_algorithms.py
   ```

## 🔑 API Keys

- **Telegram**: [@BotFather](https://t.me/botfather) → `/newbot`
- **DeepSeek**: [platform.deepseek.com](https://platform.deepseek.com) → API Keys

## 📁 Structure

```
├── bot_algorithms.py    # Main bot + LangChain integration
├── requirements.txt     # Dependencies  
├── .env                # API keys (not in repo)
└── README.md
```

## 🎯 Features

- LangChain + DeepSeek AI integration
- Async message processing
- Error handling & logging
- `/start` and `/help` commands

## 🏭 Deployment Options

**Local Development**: Run `python bot_algorithms.py`  
**Production**: Deploy to AWS/Azure or use n8n ($20/month)

## 🛠️ Troubleshooting

- **No response**: Check API keys and bot status
- **Import errors**: Activate venv, install requirements
- **API errors**: Verify keys and internet connection