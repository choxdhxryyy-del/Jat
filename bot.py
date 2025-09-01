import telebot
from telebot import types
from groq import Groq
import time

# 🔑 Apne token yahan daalo
TELEGRAM_TOKEN = "7451412892:AAGMt-KHnfZq-dgic3FyruBbETg50RKigCY"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# 🔹 User ke liye stop flag
user_stop = {}

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Help", "About", "Stop")
    bot.send_message(
        message.chat.id,
        "👋 Namaste {0.first_name}!\nMain ek AI Telegram Bot hoon.\n\n👉 Mujhe kuch bhi puchho.".format(message.from_user),
        reply_markup=markup
    )

# /about command
@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(
        message.chat.id,
        "🤖 Ye bot Groq AI (Llama 3.1) par based hai.\n"
        "💡 Banaaya gaya Python aur Telegram API se.\n"
        "🔑 Secure API key system use karta hai."
    )

# Normal text handler
@bot.message_handler(func=lambda m: True)
def chat(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # Agar Stop button dabaya
    if text.lower() == "stop":
        user_stop[chat_id] = True
        bot.send_message(chat_id, "❌ Bot ab band ho gaya. Dubara `/start` likhkar chalu karo.")
        return

    # Agar Help button dabaya
    if text.lower() == "help":
        bot.send_message(chat_id, "ℹ️ Mujhe koi bhi sawal bhejo, mai AI ke through jawab dunga.")
        return

    # Agar About button dabaya
    if text.lower() == "about":
        about(message)
        return

    # Agar user ne Stop kiya tha
    if user_stop.get(chat_id, False):
        bot.send_message(chat_id, "⚠️ Bot band hai. Dubara chalu karne ke liye /start likho.")
        return

    # Typing action dikhana
    bot.send_chat_action(chat_id, "typing")
    time.sleep(1)

    try:
        # Groq API se response
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": text}],
        )
        reply = response.choices[0].message.content.strip()

        bot.send_message(chat_id, reply)

    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error: {e}")

print("🤖 Bot chal raha hai...")
bot.polling()