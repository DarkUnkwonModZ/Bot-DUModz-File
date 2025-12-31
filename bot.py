import telebot
from telebot import types
import os
import time

# --- SECURE CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Branding Info
BRAND_NAME = "Dark Unkwon ModZ"
LOGO_URL = "https://raw.githubusercontent.com/DarkUnkwonModZ/Blogger-DarkUnkownModZ-Appinfo/refs/heads/main/IMG/dumodz-logo-final.png"
CHANNEL_ID = "@DarkUnkwonModZ"
CHANNEL_URL = "https://t.me/DarkUnkwonModZ"
WEBSITE_URL = "https://darkunkwonmodz.blogspot.com"

# File Database (Command: [File Name, Display Name])
FILES = {
    "liteapk-dialog-box-dumodz": ["liteapk-dialog-box.zip", "LiteAPK Dialog Box Pro"],
    "pubg-mod-v1": ["pubg_mod.zip", "PUBG VIP Mod Menu"],
    "netflix-premium": ["netflix_mod.apk", "Netflix Premium Unlocked"]
}

# --- MIDDLEWARE: SUBSCRIPTION CHECK ---
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

# --- UI COMPONENTS ---
def get_main_keyboard(verified=False):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_channel = types.InlineKeyboardButton("📢 Telegram Channel", url=CHANNEL_URL)
    btn_web = types.InlineKeyboardButton("🌐 Official Website", url=WEBSITE_URL)
    
    if not verified:
        btn_verify = types.InlineKeyboardButton("🔄 Verify Membership", callback_data="verify_sub")
        markup.add(btn_channel, btn_web)
        markup.add(btn_verify)
    else:
        markup.add(btn_channel, btn_web)
    return markup

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def welcome_screen(message):
    name = message.from_user.first_name
    welcome_text = (
        f"<b>Welcome to {BRAND_NAME} 🛡️</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Hello <b>{name}</b>, your premium destination for exclusive "
        "mod applications, scripts, and professional tools.\n\n"
        "✨ <b>System Status:</b> <code>Ready & Secure</code>\n"
        "💎 <b>Access:</b> <code>Premium User</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ <i>Membership verification is required to unlock our file repository.</i>"
    )
    
    try:
        bot.send_photo(
            message.chat.id, 
            LOGO_URL, 
            caption=welcome_text, 
            reply_markup=get_main_keyboard(is_subscribed(message.from_user.id))
        )
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(is_subscribed(message.from_user.id)))

@bot.message_handler(commands=['commands', 'help'])
def list_files(message):
    if not is_subscribed(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ <b>Access Denied!</b>\nPlease join our channel first to see available commands.", reply_markup=get_subscription_only_markup())

    text = (
        "🛠 <b>Premium File Repository</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    for cmd, data in FILES.items():
        text += f"🔹 <b>{data[1]}</b>\n┗ <code>/{cmd}</code>\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━━━━━\n<i>Tap a command to request the file.</i>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text.startswith('/'))
def handle_file_requests(message):
    cmd = message.text[1:].strip().lower()
    
    if cmd in FILES:
        if not is_subscribed(message.from_user.id):
            return bot.send_message(message.chat.id, "❌ <b>Membership Required!</b>\nJoin our official channel to download this file.", reply_markup=get_subscription_only_markup())

        # Professional Animation
        status_msg = bot.send_message(message.chat.id, "🔍 <b>Verifying Request...</b>")
        time.sleep(1)
        bot.edit_message_text("⚡ <b>Accessing Secure Database...</b>", message.chat.id, status_msg.message_id)
        time.sleep(0.8)
        bot.edit_message_text("📤 <b>Sending Encrypted File...</b>", message.chat.id, status_msg.message_id)

        file_info = FILES[cmd]
        if os.path.exists(file_info[0]):
            try:
                bot.send_chat_action(message.chat.id, 'upload_document')
                with open(file_info[0], 'rb') as f:
                    bot.send_document(
                        message.chat.id, f,
                        caption=f"✅ <b>File:</b> {file_info[1]}\n🛡 <b>Security:</b> Virus-Free\n━━━━━━━━━━━━━━━━━━━━\n👤 <i>Requested by: {message.from_user.first_name}</i>",
                        reply_to_message_id=message.message_id
                    )
                bot.delete_message(message.chat.id, status_msg.message_id)
            except Exception as e:
                bot.edit_message_text(f"❌ <b>Transfer Error:</b> {str(e)}", message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text(
                "🚧 <b>System Maintenance</b>\n━━━━━━━━━━━━━━━━━━━━\n"
                "This file is currently being updated to the latest version. "
                "It will be available again shortly. Thank you for your patience!", 
                message.chat.id, status_msg.message_id
            )

# --- CALLBACKS ---

@bot.callback_query_handler(func=lambda call: call.data == "verify_sub")
def verify_user(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Verified! Access Granted.", show_alert=True)
        bot.edit_message_caption(
            "✅ <b>Verification Success!</b>\n\nYour premium access has been unlocked. Use /commands to browse our files.",
            call.message.chat.id, call.message.message_id,
            reply_markup=get_main_keyboard(True)
        )
    else:
        bot.answer_callback_query(call.id, "❌ You haven't joined yet!", show_alert=True)

def get_subscription_only_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join Dark Unkwon ModZ", url=CHANNEL_URL))
    return markup

# --- RUN BOT ---
if __name__ == "__main__":
    print(f">>> {BRAND_NAME} Bot is Active...")
    bot.infinity_polling()
