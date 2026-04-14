import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot Token (Environment Variable থেকে নিবে)
TOKEN = "8445686197:AAF2WM3kqqWoyohoOoSGmseRa-uJYBJVLPU"
ADMIN_ID = 8194390770

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 দেখুন আমার Chat ID", callback_data='show_chatid')],
        [InlineKeyboardButton("📢 আপডেট চ্যানেল", url='https://t.me/earning_channel24')],
        [InlineKeyboardButton("👨‍💻 ডেভেলপার", url='https://t.me/bot_developer_io')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🤖 **চ্যাট আইডি বট এ স্বাগতম!**\n\n"
        "আপনার চ্যাট আইডি দেখতে নিচের বাটনে ক্লিক করুন।\n\n"
        "📢 আপডেট পেতে চ্যানেল জয়েন করুন\n"
        "👨‍💻 ডেভেলপার: @bot_developer_io"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# Chat ID দেখানোর হ্যান্ডলার
async def show_chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    chat_id = user.id
    username = user.username or "None"
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    
    # ইউজারের তৈরি তারিখ (Telegram এটার সরাসরি ডাটা দেয় না, একাউন্ট তৈরি তারিখ জানা যায় না)
    # পরিবর্তে বটে জয়েন করার তারিখ দেখানো হবে
    join_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # ইউজারের প্রোফাইল ছবি获取
    photo = None
    try:
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            photo = photos.photos[0][-1].file_id
    except:
        pass
    
    message_text = (
        f"🆔 **আপনার চ্যাট আইডি:** `{chat_id}`\n"
        f"👤 **নাম:** {first_name} {last_name}\n"
        f"📛 **ইউজারনেম:** @{username}\n"
        f"📅 **বটে জয়েনের তারিখ:** {join_date}\n\n"
        f"💡 কপি করে নিন আপনার Chat ID: `{chat_id}`"
    )
    
    if photo:
        await query.message.reply_photo(photo=photo, caption=message_text, parse_mode='Markdown')
    else:
        await query.message.reply_text(message_text, parse_mode='Markdown')

# ফরওয়ার্ড করা মেসেজ দেখলে Chat ID দেখাবে
async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # যদি মেসেজ ফরওয়ার্ড করা হয়
    if message.forward_origin:
        chat_id = message.chat.id
        user = message.from_user
        
        response_text = (
            f"🔍 **ফরওয়ার্ড করা মেসেজ ডিটেক্টেড!**\n\n"
            f"🆔 **আপনার Chat ID:** `{chat_id}`\n"
            f"👤 **আপনার নাম:** {user.first_name}\n\n"
            f"💡 এই Chat ID ব্যবহার করে আপনি বট কন্ট্রোল করতে পারবেন।"
        )
        await message.reply_text(response_text, parse_mode='Markdown')

# এরর হ্যান্ডলার
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error occurred: {context.error}")

def main():
    # বট তৈরি
    application = Application.builder().token(TOKEN).build()
    
    # হ্যান্ডলার যোগ
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_chatid, pattern='show_chatid'))
    application.add_handler(CommandHandler("chatid", show_chatid))  # ডিরেক্ট কমান্ড
    application.add_handler(CommandHandler("myid", show_chatid))    # অল্টারনেট কমান্ড
    application.add_handler(CommandHandler("id", show_chatid))      # শর্ট কমান্ড
    
    # ফরওয়ার্ড মেসেজ হ্যান্ডলার
    application.add_handler(CommandHandler("forward", handle_forward))
    # সব টেক্সট মেসেজ চেক করবে ফরওয়ার্ডের জন্য
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_forward))
    
    # এরর হ্যান্ডলার
    application.add_error_handler(error_handler)
    
    # বট চালু
    print("🤖 Chat ID Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
