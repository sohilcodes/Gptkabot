import os
import time
import telebot
import threading
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6411315434

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

clarity_text = """You’ll understand:
• What price movement actually represents
• Why charts behave the way they do
• Basic platform understanding
• Common beginner confusion

👉 This removes 70% confusion instantly.
"""

observation_text = """Now learn to observe.

• Identify simple trends
• Recognize sideways markets
• Watch reaction zones
• Understand behavior patterns

👉 Don’t predict — observe.
"""

thinking_text = """Now improve decision thinking.

• Why emotions create mistakes
• How to slow down decisions
• When to stay out
• Building consistency

👉 Thinking is your real edge.
"""

learn_more = """If you’ve completed the steps, you’re already ahead of most learners.

But learning alone can still feel confusing.

If you want:
• Clear explanations
• Help understanding charts
• Guidance on next steps

📩 Continue your learning here : @QXEmpire_Team

👉 Ask your questions and move forward with clarity
"""

# ===== IMAGE LINKS (channel images direct links) =====
CLARITY_IMG = "https://t.me/task25rs/79"
OBSERVATION_IMG = "https://t.me/task25rs/78"
THINKING_IMG = "https://t.me/task25rs/77"


# ===== MENU =====

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧩 Step 1: Clarity", "👁 Step 2: Observation")
    kb.row("🧠 Step 3: Thinking", "🎯 Quick Check")
    kb.row("💬 Continue")
    return kb


# ===== TYPING =====

def typing(chat_id):
    for _ in range(5):
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)


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


# ===== STEPS (IMAGE + CAPTION SAME MSG) =====

@bot.message_handler(func=lambda m: m.text == "🧩 Step 1: Clarity")
def step1(m):
    typing(m.chat.id)
    bot.send_photo(m.chat.id, CLARITY_IMG, caption=clarity_text)


@bot.message_handler(func=lambda m: m.text == "👁 Step 2: Observation")
def step2(m):
    typing(m.chat.id)
    bot.send_photo(m.chat.id, OBSERVATION_IMG, caption=observation_text)


@bot.message_handler(func=lambda m: m.text == "🧠 Step 3: Thinking")
def step3(m):
    typing(m.chat.id)
    bot.send_photo(m.chat.id, THINKING_IMG, caption=thinking_text)


@bot.message_handler(func=lambda m: m.text == "💬 Continue")
def step4(m):
    typing(m.chat.id)
    bot.send_message(m.chat.id, learn_more)


# ===== QUIZ =====

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
    typing(m.chat.id)
    q1(m.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    chat_id = call.message.chat.id

    typing(chat_id)

    if call.data == "q1_b":
        bot.send_message(chat_id, "✅ Great!! It's Correct Answer")
        q2(chat_id)
    elif call.data.startswith("q1"):
        bot.send_message(chat_id, "❌ Correct Answer: B) Observe the market")
        q2(chat_id)

    elif call.data == "q2_c":
        bot.send_message(chat_id, "✅ Great!! It's Correct Answer")
        q3(chat_id)
    elif call.data.startswith("q2"):
        bot.send_message(chat_id, "❌ Correct Answer: C) Emotions")
        q3(chat_id)

    elif call.data == "q3_b":
        bot.send_message(chat_id, "✅ Great!! It's Correct Answer")
        threading.Thread(target=final_msg, args=(chat_id,)).start()
    elif call.data.startswith("q3"):
        bot.send_message(chat_id, "❌ Correct Answer: B) Structured thinking")
        threading.Thread(target=final_msg, args=(chat_id,)).start()


# ===== FINAL MESSAGE =====

def final_msg(chat_id):
    time.sleep(3)

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
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN)
    app.run(host="0.0.0.0", port=10000)
