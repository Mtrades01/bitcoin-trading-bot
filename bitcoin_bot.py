import os
import asyncio
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Initialize Telegram Bot
bot = Bot(token=BOT_TOKEN)

async def start(update, context):
    await update.message.reply_text("Hello! I'm your Bitcoin bot.")

async def send_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("Bot is running...")
    
    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Run main() properly without asyncio.run()
    loop.run_forever()  # Keep the bot running