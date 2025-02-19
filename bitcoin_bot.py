import os
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime

# Get bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS_FILE = "chat_ids.json"

# Function to load chat IDs from file
def load_chat_ids():
    if os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save chat IDs
def save_chat_id(chat_id):
    chat_ids = load_chat_ids()
    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        with open(CHAT_IDS_FILE, "w") as file:
            json.dump(chat_ids, file)

# Command to start the bot
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    save_chat_id(chat_id)
    await update.message.reply_text("Hello! Your Bitcoin bot is active. You will receive updates.")

# Function to fetch Bitcoin price and support/resistance levels
def get_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data["bitcoin"]["usd"]
        
        # Example support/resistance levels (adjust as needed)
        support = round(price * 0.95, 2)
        resistance = round(price * 1.05, 2)
        
        return f"📊 Bitcoin Update ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):\n\n💰 Price: ${price}\n📉 Support: ${support}\n📈 Resistance: ${resistance}"
    return "Failed to fetch Bitcoin data."

# Function to send Bitcoin updates
async def send_bitcoin_update(context: CallbackContext):
    message = get_bitcoin_data()
    chat_ids = load_chat_ids()
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

# Main function to run the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))

    # Get the job queue and schedule updates
    job_queue = app.job_queue
    job_queue.run_repeating(send_bitcoin_update, interval=3600, first=10)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
