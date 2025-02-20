import logging
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot application
app = Application.builder().token(BOT_TOKEN).build()

# Function to get Bitcoin price
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url).json()
    return response["bitcoin"]["usd"]

# Command: Start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I will send you Bitcoin updates.")

# Command: Price
async def bitcoin_price(update: Update, context: CallbackContext):
    price = get_bitcoin_price()
    await update.message.reply_text(f"Current Bitcoin price: ${price}")

# Function to send Bitcoin price updates
async def send_bitcoin_update(context: CallbackContext):
    chat_id = context.job.chat_id
    price = get_bitcoin_price()
    await context.bot.send_message(chat_id=chat_id, text=f"Bitcoin price update: ${price}")

# Command: Subscribe to updates
async def subscribe(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(send_bitcoin_update, interval=3600, first=10, chat_id=chat_id)
    await update.message.reply_text("You will receive Bitcoin price updates every hour.")

# Set up command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", bitcoin_price))
app.add_handler(CommandHandler("subscribe", subscribe))

# Start the bot
async def main():
    logger.info("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())