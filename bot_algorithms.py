import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize DeepSeek LLM with OpenAI-compatible interface
llm = ChatOpenAI(
    openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
    openai_api_base="https://api.deepseek.com/v1",
    model_name="deepseek-chat",
    temperature=0.3
)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! I am Vic GUROV\'s AI agent powered by DeepSeek. 🤖\n'
        'Ask me any question and I\'ll help you with an intelligent response.'
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 *AI Telegram Bot Commands*

/start - Start the bot
/help - Show this help message

Just send me any text message and I'll respond with AI-powered answers using DeepSeek!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle text messages with DeepSeek AI."""
    user_message = update.message.text or ""
    user_name = update.effective_user.first_name if update.effective_user else "Unknown"
    chat_id = update.effective_chat.id if update.effective_chat else None

    # Rate limiting: allow one message per 2 seconds per user (simple in-memory)
    if not hasattr(context, 'user_data'):
        context.user_data = {}
    last_time = context.user_data.get('last_message_time', 0)
    import time
    now = time.time()
    if now - last_time < 2:
        await update.message.reply_text("⏳ Please wait a moment before sending another message.")
        return
    context.user_data['last_message_time'] = now

    # Input validation
    if not user_message.strip():
        await update.message.reply_text("⚠️ Please send a non-empty message.")
        return
    if len(user_message.strip()) < 2:
        await update.message.reply_text("⚠️ Your message is too short. Please provide more details.")
        return

    # Multi-language support (detect language, respond accordingly)
    import langdetect
    try:
        lang = langdetect.detect(user_message)
    except Exception:
        lang = "en"

    # Custom prompt support (simple role setting)
    role = context.user_data.get('role', None)
    prompt = user_message
    if role:
        prompt = f"You are a helpful assistant. Role: {role}. User says: {user_message}"

    # Log the incoming message
    logger.info(f"User {user_name} ({lang}): {user_message}")

    try:
        # User feedback: show processing message
        await update.message.reply_text("🤔 Thinking...", quote=True)
        # Send "typing" action to show bot is processing
        if chat_id:
            await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        # Get response from DeepSeek
        response = await llm.agenerate([[HumanMessage(content=prompt)]])
        ai_response = response.generations[0][0].text

        # Response formatting: Markdown support
        await update.message.reply_text(ai_response, parse_mode='Markdown')

        # Log the AI response
        logger.info(f"AI Response: {ai_response[:100]}...")

    except Exception as e:
        import traceback
        logger.error(f"Error processing message: {str(e)}\n{traceback.format_exc()}")
        await update.message.reply_text(
            "Sorry, I encountered an error while processing your message. Please try again later."
        )

def main() -> None:
    """Start the bot."""
    # Get bot token from environment
    bot_token = os.getenv('YOUR_TELEGRAM_BOT_TOKEN')
    if not bot_token:
        raise ValueError("YOUR_TELEGRAM_BOT_TOKEN not found in environment variables")
    
    # Check for DeepSeek API key
    if not os.getenv('DEEPSEEK_API_KEY'):
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
    
    # Create the Application
    application = Application.builder().token(bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Starting Vic GUROV\'s AI elegram Bot powered by DeepSeek.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()