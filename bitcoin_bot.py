import asyncio
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# Initialize the bot application
app = Application.builder().token(BOT_TOKEN).build()

# Command handler: /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your Bitcoin Trading Bot.")

# Add handlers
app.add_handler(CommandHandler("start", start))

# Main function
async def main():
    logger.info("Bot is running...")
    await app.run_polling()

# Fix for "RuntimeError: This event loop is already running"
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())