import telebot
from telebot import types
import os
import time

# GitHub Secrets থেকে ডাটা নিবে
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID') # তোমার আইডি দাও (ঐচ্ছিক)

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- CONFIGURATION ---
CHANNELS = [
    {"name": "DUMoDZ Official", "url": "https://t.me/DemoTestDUModz", "id": "@DemoTestDUModz"}
]

# File Database
FILES = {
    "liteapk-dialog-box-dumodz": ["liteapk-dialog-box.zip", "Premium LiteAPK Dialog Box"],
    "pubg-mod-v1": ["pubg_mod.zip", "PUBG VIP Mod Menu"],
    "netflix-premium": ["netflix_mod.apk", "Netflix Unlocked Premium"]
}

# --- HELPERS ---
def is_subscribed(user_id):
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch['id'], user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

def get_sub_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        markup.add(types.InlineKeyboardButton(f"📢 Join {ch['name']}", url=ch['url']))
    markup.add(types.InlineKeyboardButton("🔄 Verify Membership", callback_data="verify"))
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        f"<b>Hello, {message.from_user.first_name}! 👋</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 <b>DUMoDZ Cloud System</b>\n"
        "Premium files are ready for you.\n\n"
        "✅ <b>Status:</b> <code>Active via GitHub Actions</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    if is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"{welcome}\n\nUse /commands to access files.")
    else:
        bot.send_message(message.chat.id, welcome, reply_markup=get_sub_keyboard())

@bot.message_handler(commands=['commands'])
def cmds(message):
    if not is_subscribed(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ Join first!", reply_markup=get_sub_keyboard())
    
    text = "🛠 <b>Available Repository:</b>\n\n"
    for cmd, data in FILES.items():
        text += f"💎 <b>{data[1]}</b>\n┗ <code>/{cmd}</code>\n\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text.startswith('/'))
def handle_files(message):
    cmd = message.text[1:].strip().lower()
    if cmd in FILES:
        if not is_subscribed(message.from_user.id):
            return bot.send_message(message.chat.id, "❌ Join required!", reply_markup=get_sub_keyboard())

        # Professional Animation
        status = bot.send_message(message.chat.id, "📡 <b>Connecting to GitHub Server...</b>")
        time.sleep(1)
        bot.edit_message_text("🔓 <b>Authenticating Access...</b>", message.chat.id, status.message_id)
        time.sleep(1)
        bot.edit_message_text("📤 <b>Sending Premium File...</b>", message.chat.id, status.message_id)

        file_name = FILES[cmd][0]
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                bot.send_document(message.chat.id, f, caption=f"✅ <b>File:</b> {FILES[cmd][1]}\n👤 Requested by: {message.from_user.first_name}")
            bot.delete_message(message.chat.id, status.message_id)
        else:
            bot.edit_message_text("🚧 <b>File Missing!</b>\nPlease upload the file to your GitHub repository first.", message.chat.id, status.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_cb(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Verified!", show_alert=True)
        bot.edit_message_text("✅ <b>Access Granted!</b>\nYou can now use /commands.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ Join the channel first!", show_alert=True)

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()