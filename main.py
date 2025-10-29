from flask import Flask, send_from_directory
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import firebase_admin
from firebase_admin import credentials, firestore
import os, threading, time
import imghdr

# Initialize Flask
app = Flask(__name__)

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Telegram bot setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

# Telegram Commands
def start(update, context):
    user = update.effective_user
    user_id = str(user.id)

    user_ref = db.collection("users").document(user_id)
    if not user_ref.get().exists:
        user_ref.set({"coins": 0, "insta_done": False, "fb_done": False, "x_done": False})

    keyboard = [
        [InlineKeyboardButton("🚀 Open Chill Miner", url="https://your-app-name.onrender.com")]
    ]
    update.message.reply_text(
        "👋 Welcome to *Chill Miner!*\n\nTap below to open the mining dashboard ⬇️",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def balance(update, context):
    user_id = str(update.effective_user.id)
    user_ref = db.collection("users").document(user_id).get()
    if user_ref.exists:
        coins = user_ref.to_dict().get("coins", 0)
        update.message.reply_text(f"💎 You have {coins} Chill Coins.")
    else:
        update.message.reply_text("Start first with /start")

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("balance", balance))

# Flask Routes for Web App
@app.route('/')
def home():
    return send_from_directory('web', 'index.html')

@app.route('/about')
def about():
    return send_from_directory('web', 'about.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('web', path)

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def run_telegram():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_telegram).start()
