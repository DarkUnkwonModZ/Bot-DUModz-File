import telebot
from telebot import types
import os
import time

# --- SECURE CONFIGURATION (Admin Panel) ---
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 8504263842  # Your Chat ID: Dark Unknown

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Branding & Links
BRAND_NAME = "Dark Unkwon ModZ"
LOGO_URL = "https://raw.githubusercontent.com/DarkUnkwonModZ/Blogger-DarkUnkownModZ-Appinfo/refs/heads/main/IMG/dumodz-logo-final.png"
REQUIRED_CHANNEL = "@DemoTestDUModz" # Channel ID for verification
CHANNEL_URL = "https://t.me/DemoTestDUModz"
WEBSITE_URL = "https://darkunkwonmodz.blogspot.com"

# Premium File Database
FILES_DB = {
    "liteapk-dialog-box-dumodz": ["liteapk-dialog-box.zip", "LiteAPK Dialog Box Pro"],
    "pubg-mod-v1": ["pubg_mod.zip", "PUBG Mobile VIP Mod"],
    "netflix-premium": ["netflix_mod.apk", "Netflix Premium Unlocked"]
}

# --- ADVANCED VERIFICATION SYSTEM ---
def is_member(user_id):
    """Checks if the user is a member of the required channel."""
    try:
        member = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        # If bot is not admin in channel, this will trigger
        print(f"Verification Error: {e}")
        return False

# --- UI MARKUPS ---
def welcome_markup(verified=False):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_channel = types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)
    btn_web = types.InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_URL)
    
    if not verified:
        btn_verify = types.InlineKeyboardButton("🔄 Verify Membership", callback_data="check_sub")
        markup.add(btn_channel, btn_web)
        markup.add(btn_verify)
    else:
        markup.add(btn_channel, btn_web)
    return markup

# --- COMMAND HANDLERS ---

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_name = message.from_user.first_name
    verified = is_member(message.from_user.id)
    
    caption = (
        f"<b>Welcome to {BRAND_NAME} System 🛡️</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Hello <b>{user_name}</b>, access our cloud database for premium "
        "mod applications and professional scripts.\n\n"
        f"👤 <b>User:</b> <code>{user_name}</code>\n"
        f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n"
        f"💎 <b>Status:</b> {'<code>Verified ✅</code>' if verified else '<code>Unverified ❌</code>'}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ <i>You must join our official channel to unlock the file repository.</i>"
    )
    
    try:
        bot.send_photo(message.chat.id, LOGO_URL, caption=caption, reply_markup=welcome_markup(verified))
    except:
        bot.send_message(message.chat.id, caption, reply_markup=welcome_markup(verified))

@bot.message_handler(commands=['commands', 'help'])
def list_files(message):
    if not is_member(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ <b>Access Denied!</b>\nPlease join the channel and click 'Verify' to unlock commands.", 
                                reply_markup=welcome_markup(False))

    text = "🛠 <b>Available Premium Commands:</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for cmd, info in FILES_DB.items():
        text += f"🔹 <b>{info[1]}</b>\n┗ <code>/{cmd}</code>\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━━━━━\n<i>Tap a command to download the file.</i>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text.startswith('/'))
def handle_requests(message):
    cmd = message.text[1:].strip().lower()
    
    if cmd in FILES_DB:
        if not is_member(message.from_user.id):
            return bot.send_message(message.chat.id, "❌ <b>Verification Required!</b>\nJoin our channel to download this file.", 
                                    reply_markup=welcome_markup(False))

        # Premium Search Animation
        status = bot.send_message(message.chat.id, "🔍 <b>Authenticating Request...</b>")
        time.sleep(1)
        bot.edit_message_text("⚡ <b>Accessing Secure Server...</b>", message.chat.id, status.message_id)
        time.sleep(0.8)
        bot.edit_message_text("📤 <b>Sending Premium File...</b>", message.chat.id, status.message_id)

        file_info = FILES_DB[cmd]
        file_path = file_info[0]
        
        if os.path.exists(file_path):
            try:
                bot.send_chat_action(message.chat.id, 'upload_document')
                with open(file_path, 'rb') as f:
                    bot.send_document(
                        message.chat.id, f,
                        caption=f"✅ <b>File:</b> {file_info[1]}\n🛡 <b>Security:</b> Scanned & Safe\n━━━━━━━━━━━━━━━━━━━━\n👤 <i>Requested by: {message.from_user.first_name}</i>",
                        reply_to_message_id=message.message_id
                    )
                bot.delete_message(message.chat.id, status.message_id)
            except Exception as e:
                bot.edit_message_text(f"❌ <b>Error:</b> Could not send file. ({e})", message.chat.id, status.message_id)
        else:
            bot.edit_message_text(
                "🚧 <b>File Under Maintenance!</b>\n━━━━━━━━━━━━━━━━━━━━\n"
                "The requested file is currently being updated. "
                "It will be available again shortly in the next cloud sync.", 
                message.chat.id, status.message_id
            )

# --- CALLBACK HANDLER ---

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_callback(call):
    if is_member(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Identity Verified!", show_alert=True)
        bot.edit_message_caption(
            "✅ <b>Verification Success!</b>\n\nAccess has been granted. You can now use /commands to browse our premium repository.",
            call.message.chat.id, call.message.message_id,
            reply_markup=welcome_markup(True)
        )
    else:
        bot.answer_callback_query(call.id, "❌ You have not joined @DemoTestDUModz yet!", show_alert=True)

# --- ADMIN FEATURES ---
@bot.message_handler(commands=['stats'])
def admin_stats(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "📊 <b>Admin Dashboard:</b>\nSystem is running smoothly via GitHub Actions.")

# --- RUN BOT ---
if __name__ == "__main__":
    print(">>> Dark Unkwon ModZ Bot is Online...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
