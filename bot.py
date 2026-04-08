import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# ===== ENV VARIABLES =====
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "6411315434"))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")  # your Render URL

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
users = {}

# ===== TEXT CONTENT =====
disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in losses.

We do not provide financial advice, signals, or guaranteed outcomes.

All content is for learning and informational use only.
These are projections and not guarantees.

By continuing, you confirm that you understand and accept this.
"""

welcome = """Welcome 👋  

This is a structured learning space designed to help you understand how financial markets and trading platforms work in a clear and simple way.

No shortcuts. No confusing terms.  
Only step-by-step explanations, practical examples, and focused learning.

You will explore how price moves, how markets behave, and how to build a strong foundation through observation and structured thinking.

Take your time, follow each section, and focus on understanding.

⚠️ Educational purposes only.  
We do not provide financial advice.  
These are projections and not guarantees.

👇 Choose a section below to begin.
"""

clarity_text = "🧠 Clarity content..."  # your clarity_text
observation_text = "👀 Observation content..."  # your observation_text
thinking_text = "💭 Thinking content..."  # your thinking_text
faq_text = "FAQ content..."
support_text = "Support content..."

# ===== IMAGE LINKS =====
CLARITY_IMG = "https://t.me/task25rs/79"
OBSERVATION_IMG = "https://t.me/task25rs/78"
THINKING_IMG = "https://t.me/task25rs/77"

# ===== MENU =====
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧩 Step 1: Clarity", "👁 Step 2: Observation")
    kb.row("🧠 Step 3: Thinking", "🎯 Quick Check")
    kb.row("❓ FAQ", "📩 Support")
    return kb

# ===== START =====
@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.from_user.id
    if uid not in users:
        users[uid] = {}
        bot.send_message(ADMIN_ID, f"🆕 New User\nID: {uid}\nName: {msg.from_user.first_name}")
        d = bot.send_message(msg.chat.id, disclaimer)
        try:
            bot.pin_chat_message(msg.chat.id, d.message_id)
        except:
            pass
    bot.send_message(msg.chat.id, welcome, reply_markup=menu())

# ===== STEP HANDLERS =====
@bot.message_handler(func=lambda m: "Step 1" in m.text)
def step1(m):
    bot.send_photo(m.chat.id, CLARITY_IMG, caption=clarity_text)

@bot.message_handler(func=lambda m: "Step 2" in m.text)
def step2(m):
    bot.send_photo(m.chat.id, OBSERVATION_IMG, caption=observation_text)

@bot.message_handler(func=lambda m: "Step 3" in m.text)
def step3(m):
    bot.send_photo(m.chat.id, THINKING_IMG, caption=thinking_text)

# ===== FAQ & SUPPORT =====
@bot.message_handler(func=lambda m: "FAQ" in m.text)
def faq(m):
    bot.send_message(m.chat.id, faq_text)

@bot.message_handler(func=lambda m: "Support" in m.text)
def support(m):
    bot.send_message(m.chat.id, support_text)

# ===== QUIZ =====
def q1(chat_id):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("A) To act quickly without thinking", callback_data="q1_a"),
        InlineKeyboardButton("B) To understand before taking action", callback_data="q1_b"),
        InlineKeyboardButton("C) To follow others blindly", callback_data="q1_c")
    )
    bot.send_message(chat_id,
        "🧪 Quick Check – Question 1\nWhat is the purpose of clarity in market learning?\n👉 Select your answer below:",
        reply_markup=kb
    )

def q2(chat_id):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("A) React instantly", callback_data="q2_a"),
        InlineKeyboardButton("B) Understand patterns & behavior", callback_data="q2_b"),
        InlineKeyboardButton("C) Guarantees outcomes", callback_data="q2_c")
    )
    bot.send_message(chat_id,
        "🧪 Quick Check – Question 2\nWhy is observation important?\n👉 Select your answer below:",
        reply_markup=kb
    )

def q3(chat_id):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("A) Make emotional decisions", callback_data="q3_a"),
        InlineKeyboardButton("B) Avoid planning", callback_data="q3_b"),
        InlineKeyboardButton("C) Analyze situations before acting", callback_data="q3_c")
    )
    bot.send_message(chat_id,
        "🧪 Quick Check – Question 3\nWhat does structured thinking help you do?\n👉 Select your answer below:",
        reply_markup=kb
    )

@bot.message_handler(func=lambda m: "Quick Check" in m.text)
def start_quiz(m):
    q1(m.chat.id)

# ===== CALLBACK HANDLER =====
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    chat_id = call.message.chat.id
    if call.data.startswith("q1"):
        if call.data == "q1_b":
            bot.send_message(chat_id, "✅ Correct! Clarity helps you understand before acting.\n👉 Next question:")
        else:
            bot.send_message(chat_id, "❌ Not quite. Clarity is about understanding before action.\n👉 Next question:")
        q2(chat_id)

    elif call.data.startswith("q2"):
        if call.data == "q2_b":
            bot.send_message(chat_id, "✅ Correct! Observation helps recognize patterns over time.\n👉 Next question:")
        else:
            bot.send_message(chat_id, "❌ Not exactly. Observation is about understanding patterns.\n👉 Final question:")
        q3(chat_id)

    elif call.data.startswith("q3"):
        if call.data == "q3_c":
            bot.send_message(chat_id, "✅ Correct! Structured thinking helps analyze situations calmly.\n🎉 Quiz completed!")
        else:
            bot.send_message(chat_id, "❌ Not correct. Thinking is about analyzing before acting.\n🎉 Quiz completed!")
        bot.send_message(chat_id, "⚠️ Educational purposes only.\n👉 Explore FAQ to continue learning.")

# ===== WEBHOOK =====
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "Bot Running"

# ===== RUN =====
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
