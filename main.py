import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from datetime import datetime
import threading

# Bot Token
BOT_TOKEN = "8445686197:AAF2WM3kqqWoyohoOoSGmseRa-uJYBJVLPU"
ADMIN_ID = 8194390770

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# /start কমান্ড
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("👤 দেখুন আমার Chat ID", callback_data='show_chatid')
    btn2 = InlineKeyboardButton("📢 আপডেট চ্যানেল", url='https://t.me/earning_channel24')
    btn3 = InlineKeyboardButton("👨‍💻 ডেভেলপার", url='https://t.me/bot_developer_io')
    keyboard.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id, 
        f"🤖 হ্যালো {user.first_name}!\n\nআমি চ্যাট আইডি বট 🔥\n\nআপনার চ্যাট আইডি দেখতে নিচের বাটনে ক্লিক করুন।", 
        reply_markup=keyboard
    )

# বাটন ক্লিক করলে Chat ID দেখাবে
@bot.callback_query_handler(func=lambda call: call.data == 'show_chatid')
def show_chatid(call):
    user = call.from_user
    chat_id = user.id
    username = user.username or "None"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    current_time = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    
    msg = f"🆔 আপনার Chat ID: {chat_id}\n\n👤 নাম: {full_name}\n📛 ইউজারনাম: @{username}\n📅 তারিখ: {current_time}"
    
    # প্রোফাইল ছবি দেখানোর চেষ্টা
    try:
        photos = bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            bot.send_photo(call.message.chat.id, photos.photos[0][-1].file_id, caption=msg)
        else:
            bot.send_message(call.message.chat.id, msg)
    except:
        bot.send_message(call.message.chat.id, msg)
    
    bot.answer_callback_query(call.id)

# সরাসরি কমান্ড
@bot.message_handler(commands=['myid', 'chatid', 'id'])
def get_id(message):
    bot.reply_to(message, f"🆔 আপনার Chat ID: {message.chat.id}")

# ফরওয়ার্ড মেসেজ ধরবে
@bot.message_handler(func=lambda m: m.forward_origin is not None)
def forward_handler(message):
    bot.reply_to(message, f"🔄 ফরওয়ার্ড মেসেজ!\n\n🆔 আপনার Chat ID: {message.chat.id}")

# Flask রুট
@app.route('/')
def home():
    return "Chat ID Bot is Running!"

# বট চালু
def run_bot():
    print("Bot started...")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8080)
