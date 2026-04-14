import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token (সরাসরি দেওয়া)
TOKEN = "8445686197:AAF2WM3kqqWoyohoOoSGmseRa-uJYBJVLPU"
ADMIN_ID = 8194390770

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("👤 দেখুন আমার Chat ID", callback_data='show_chatid')],
        [InlineKeyboardButton("📢 আপডেট চ্যানেল", url='https://t.me/earning_channel24')],
        [InlineKeyboardButton("👨‍💻 ডেভেলপার", url='https://t.me/bot_developer_io')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"🤖 **হ্যালো {user.first_name}!**\n\n"
        "আমি চ্যাট আইডি বট 🔥\n"
        "আপনার চ্যাট আইডি দেখতে নিচের বাটনে ক্লিক করুন।\n\n"
        "📢 আপডেট পেতে চ্যানেল জয়েন করুন\n"
        "👨‍💻 ডেভেলপার: @bot_developer_io"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# Chat ID দেখানো
async def show_chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    chat_id = user.id
    username = user.username or "None"
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    
    # বর্তমান তারিখ
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    message_text = (
        f"🆔 **আপনার Chat ID:** `{chat_id}`\n"
        f"👤 **নাম:** {first_name} {last_name}\n"
        f"📛 **ইউজারনেম:** @{username}\n"
        f"📅 **তারিখ:** {current_date}\n\n"
        f"✅ কপি করুন: `{chat_id}`"
    )
    
    # প্রোফাইল ছবি পাওয়ার চেষ্টা
    try:
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            photo = photos.photos[0][-1].file_id
            await query.message.reply_photo(photo=photo, caption=message_text, parse_mode='Markdown')
        else:
            await query.message.reply_text(message_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Photo error: {e}")
        await query.message.reply_text(message_text, parse_mode='Markdown')

# ফরওয়ার্ড মেসেজ হ্যান্ডলার
async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # চেক করি মেসেজ ফরওয়ার্ড কিনা
    if message.forward_origin:
        chat_id = message.chat.id
        user = message.from_user
        
        response_text = (
            f"🔄 **ফরওয়ার্ড মেসেজ!**\n\n"
            f"🆔 **আপনার Chat ID:** `{chat_id}`\n"
            f"👤 **নাম:** {user.first_name}\n\n"
            f"💡 এই Chat ID টি আপনার বটের জন্য ব্যবহার করুন।"
        )
        await message.reply_text(response_text, parse_mode='Markdown')

# সরাসরি কমান্ড দিয়ে Chat ID দেখানো
async def get_my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    text = f"🆔 **আপনার Chat ID:** `{chat_id}`\n👤 **ইউজার:** {user.first_name}"
    await update.message.reply_text(text, parse_mode='Markdown')

# অ্যাডমিন প্যানেল (ঐচ্ছিক)
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ আপনি অ্যাডমিন নন!")
        return
    
    keyboard = [
        [InlineKeyboardButton("📊 বট তথ্য", callback_data='bot_stats')],
        [InlineKeyboardButton("👥 ইউজার কাউন্ট", callback_data='user_count')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔧 **অ্যাডমিন প্যানেল**", reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'bot_stats':
        await query.message.reply_text("🤖 বট অনলাইন আছে!\n✅ সব ঠিকঠাক কাজ করছে।")
    elif query.data == 'user_count':
        await query.message.reply_text("📊 বর্তমানে নির্দিষ্ট ইউজার কাউন্ট দেখানো সম্ভব নয়।")

# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """বট চালু করার ফাংশন"""
    try:
        # Application তৈরি (সরাসরি token সহ)
        application = Application.builder().token(TOKEN).build()
        
        # হ্যান্ডলার যোগ
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("myid", get_my_id))
        application.add_handler(CommandHandler("chatid", get_my_id))
        application.add_handler(CommandHandler("id", get_my_id))
        application.add_handler(CommandHandler("admin", admin_panel))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(show_chatid, pattern='show_chatid'))
        application.add_handler(CallbackQueryHandler(button_handler, pattern='^(bot_stats|user_count)$'))
        
        # Message handlers
        from telegram.ext import MessageHandler, filters
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_forward))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        # বট চালু
        logger.info("🤖 Chat ID Bot is starting...")
        print("✅ Bot is running! Press Ctrl+C to stop.")
        
        # Polling start
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
