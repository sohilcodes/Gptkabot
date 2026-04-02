import os
import time
import telebot
import threading
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not found")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

users = {}

# ===== TEXT =====

disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this.
"""

welcome = """Welcome 👋

This is a structured learning space designed to help you understand how trading platforms work — step by step.

No shortcuts. No confusion.
Just clear thinking and practical understanding.

Follow the sections below in order 👇
"""

clarity = """🧩 Clarity

You’ll understand:
• What price movement represents
• Why charts behave this way
• Basic platform understanding
• Common beginner confusion

👉 This removes confusion instantly.
"""

observation = """👁 Observation

• Identify trends
• Recognize sideways markets
• Watch reaction zones
• Understand behavior

👉 Don’t predict — observe.
"""

thinking = """🧠 Thinking

• Emotions cause mistakes
• Slow down decisions
• Know when to stay out
• Build consistency

👉 Thinking is your real edge.
"""

learn_more = """🎯 Learn More

If you’ve completed the steps, you’re ahead of most.

📩 Continue here: @QXEmpire_Team
"""

# ===== MENU =====

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧩 Step 1: Clarity", "👁 Step 2: Observation")
    kb.row("🧠 Step 3: Thinking", "🎯 Quick Check")
    kb.row("💬 Continue")
    return kb


# ===== TYPING EFFECT =====

def typing(chat_id):
    for _ in range(5):
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)


# ===== START =====

@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.from_user.id

    if uid not in users:
        users[uid] = {"steps": set(), "quiz": 0}

        d = bot.send_message(msg.chat.id, disclaimer)
        try:
            bot.pin_chat_message(msg.chat.id, d.message_id)
        except:
            pass

    bot.send_message(msg.chat.id, welcome, reply_markup=menu())


# ===== STEPS =====

@bot.message_handler(func=lambda m: m.text == "🧩 Step 1: Clarity")
def s1(m):
    typing(m.chat.id)
    bot.send_message(m.chat.id, clarity)

@bot.message_handler(func=lambda m: m.text == "👁 Step 2: Observation")
def s2(m):
    typing(m.chat.id)
    bot.send_message(m.chat.id, observation)

@bot.message_handler(func=lambda m: m.text == "🧠 Step 3: Thinking")
def s3(m):
    typing(m.chat.id)
    bot.send_message(m.chat.id, thinking)

@bot.message_handler(func=lambda m: m.text == "💬 Continue")
def s4(m):
    typing(m.chat.id)
    bot.send_message(m.chat.id, learn_more)


# ===== QUIZ SYSTEM =====

def q1(chat_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("A) Act fast", callback_data="q1_a"),
        InlineKeyboardButton("B) Observe the market", callback_data="q1_b"),
        InlineKeyboardButton("C) Follow others", callback_data="q1_c")
    )
    bot.send_message(chat_id, "Question 1:\n\nWhat is the first step before making any decision?", reply_markup=kb)

def q2(chat_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("A) Charts", callback_data="q2_a"),
        InlineKeyboardButton("B) Strategy", callback_data="q2_b"),
        InlineKeyboardButton("C) Emotions", callback_data="q2_c")
    )
    bot.send_message(chat_id, "Question 2:\n\nWhat causes most mistakes?", reply_markup=kb)

def q3(chat_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("A) Random actions", callback_data="q3_a"),
        InlineKeyboardButton("B) Structured thinking", callback_data="q3_b")
    )
    bot.send_message(chat_id, "Question 3:\n\nWhat is better?", reply_markup=kb)


@bot.message_handler(func=lambda m: m.text == "🎯 Quick Check")
def start_quiz(m):
    users[m.from_user.id]["quiz"] = 1
    typing(m.chat.id)
    q1(m.chat.id)


# ===== ANSWERS =====

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    uid = call.from_user.id

    typing(call.message.chat.id)

    if call.data == "q1_b":
        bot.send_message(call.message.chat.id, "✅ Great! Correct Answer")
        q2(call.message.chat.id)
    elif call.data.startswith("q1"):
        bot.send_message(call.message.chat.id, "❌ Correct Answer: B) Observe the market")
        q2(call.message.chat.id)

    elif call.data == "q2_c":
        bot.send_message(call.message.chat.id, "✅ Great! Correct Answer")
        q3(call.message.chat.id)
    elif call.data.startswith("q2"):
        bot.send_message(call.message.chat.id, "❌ Correct Answer: C) Emotions")
        q3(call.message.chat.id)

    elif call.data == "q3_b":
        bot.send_message(call.message.chat.id, "✅ Great! Correct Answer")
        threading.Thread(target=final_msg, args=(call.message.chat.id,)).start()
    elif call.data.startswith("q3"):
        bot.send_message(call.message.chat.id, "❌ Correct Answer: B) Structured thinking")
        threading.Thread(target=final_msg, args=(call.message.chat.id,)).start()


# ===== FINAL MESSAGE =====

def final_msg(chat_id):
    time.sleep(3)

    # typing feel before final msg
    for _ in range(2):
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)

    bot.send_message(chat_id, """👉 If you got confused in any answer…
you should revisit the sections or ask for help 👇

📩 @QXEmpire_Team""")


# ===== WEBHOOK =====

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok", 200


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(
        url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN
    )
    app.run(host="0.0.0.0", port=10000)
