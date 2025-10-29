import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask server for Render keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "💎 Chill Miner Bot is Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# Start Flask thread
Thread(target=run_flask).start()

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_ref = db.collection("users").document(str(user.id))
    user_data = user_ref.get()

    if not user_data.exists:
        user_ref.set({"coins": 0, "username": user.username or "Unknown"})

    keyboard = [
        [InlineKeyboardButton("🪙 Mine Coins", callback_data="mine")],
        [InlineKeyboardButton("🎯 Tasks (Earn More)", callback_data="tasks")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💎 Welcome to *Chill Miner!*\nStart mining and completing tasks to earn coins 🔥",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# Mine coins
async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_ref = db.collection("users").document(str(query.from_user.id))
    user_data = user_ref.get()

    coins = user_data.to_dict().get("coins", 0) + 5
    user_ref.update({"coins": coins})

    await query.edit_message_text(
        f"⛏️ You mined 5 coins!\n💰 Total Balance: *{coins} coins*",
        parse_mode="Markdown"
    )

# Tasks section
async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/chillb0oi?igsh=MWllcTNrdDJpdXlxcw==")],
        [InlineKeyboardButton("📘 Facebook", url="https://www.facebook.com/share/1DQzvSudFP/")],
        [InlineKeyboardButton("𝕏 Twitter", url="https://x.com/CHILLB00i?t=TPYjr3Es2NF37nDG2hWU0g&s=09")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🔥 Complete these tasks and earn bonus coins by following us on all platforms 👇",
        reply_markup=reply_markup
    )

# About page
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    about_text = (
        "💎 *About Chill Miner*\n\n"
        "Chill Miner is a fun Telegram bot where you can mine coins, complete social tasks, "
        "and grow your balance easily!\n\n"
        "🔹 No investment required\n"
        "🔹 Earn coins by mining & tasks\n"
        "🔹 More features coming soon ⚡"
    )
    await query.edit_message_text(about_text, parse_mode="Markdown")

# Run bot
if __name__ == "__main__":
    import asyncio
    import threading

    async def run_bot():
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(mine, pattern="mine"))
        application.add_handler(CallbackQueryHandler(tasks, pattern="tasks"))
        application.add_handler(CallbackQueryHandler(about, pattern="about"))
        print("🤖 Chill Miner is live and polling...")
        await application.run_polling()

    def run_asyncio_loop():
        asyncio.run(run_bot())

    # Run the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_asyncio_loop)
    bot_thread.start()

    # Run the Flask server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
