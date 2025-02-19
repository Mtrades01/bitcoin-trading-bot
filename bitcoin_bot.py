import requests
import schedule
import time
import numpy as np
import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load secrets from GitHub Actions environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Store users who start the bot
USER_CHAT_IDS = set()

def start(update: Update, context: CallbackContext):
    """Handles /start command and saves the user chat ID."""
    chat_id = update.effective_chat.id
    USER_CHAT_IDS.add(chat_id)
    update.message.reply_text("✅ You are now subscribed to Bitcoin updates!")

def get_bitcoin_data():
    """Fetch historical Bitcoin price data"""
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "7", "interval": "hourly"}
    
    response = requests.get(url, params=params)
    data = response.json()

    if "prices" not in data:
        print("Error fetching Bitcoin data:", data)
        return []

    return [entry[1] for entry in data["prices"]][-100:]

def analyze_price_action(prices):
    """Analyze price action for key insights"""
    if not prices:
        return None

    current_price = prices[-1]
    recent_high = max(prices[-50:])
    recent_low = min(prices[-50:])
    volatility = round(np.std(prices[-50:]), 2)

    trend = (
        "📈 *Uptrend* - Buyers in control" if current_price > np.mean(prices[-50:])
        else "📉 *Downtrend* - Sellers in control"
    )

    return {
        "current_price": round(current_price, 2),
        "trend": trend,
        "support": round(recent_low, 2),
        "resistance": round(recent_high, 2),
        "volatility": volatility
    }

def send_message(text):
    """Send a message to all users"""
    bot = Bot(token=BOT_TOKEN)
    for chat_id in USER_CHAT_IDS:
        bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

def send_bitcoin_update():
    """Send the Bitcoin update"""
    prices = get_bitcoin_data()
    insights = analyze_price_action(prices)

    if not insights:
        print("Skipping message due to missing data.")
        return

    message = (
        f"📊 *Bitcoin Daily Price Action* 📊\n\n"
        f"💰 *Current Price:* ${insights['current_price']}\n"
        f"{insights['trend']}\n"
        f"🟢 *Support:* ${insights['support']}\n"
        f"🔴 *Resistance:* ${insights['resistance']}\n"
        f"📊 *Volatility:* {insights['volatility']}\n\n"
        f"⚡️ *Trading Tip:* Look for price action signals around key levels!"
    )

    send_message(message)

# Set up the bot
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# Schedule daily update
schedule.every().day.at("08:00").do(send_bitcoin_update)

# Start the bot
updater.start_polling()

while True:
    schedule.run_pending()
    time.sleep(60)
