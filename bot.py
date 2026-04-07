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

clarity_text = """🧠 Clarity

Clarity in trading means understanding what you are doing before taking any action.

Before entering a trade, always ask:
• Do I understand the market direction?
• Am I following a clear plan?
• Am I avoiding emotional decisions?

Clear thinking helps reduce mistakes and improves decision-making over time.

Focus on simple strategies and avoid overcomplicating the process.

“These are projections and not guarantees.”
"""

observation_text = """👀 Observation

Observation is the ability to carefully watch how the market moves.

Key things to observe:
• Price movement
• Trends (uptrend or downtrend)
• Support and resistance levels

Do not rush into trades. Spend time watching and understanding patterns.

Good observation leads to better timing and smarter decisions.

“These are projections and not guarantees.”
"""

thinking_text = """💭 Thinking

Thinking in trading means analyzing before acting.

Always consider:
• Why am I entering this trade?
• What is my risk?
• What is my exit plan?

Avoid impulsive decisions. Take time to think logically instead of reacting emotionally.

Consistent thinking improves long-term learning.

“These are projections and not guarantees.”
"""

faq_text = """❓ Frequently Asked Questions (FAQ)

1. What is this bot about?
This bot provides basic educational content about trading and how markets work.

---

2. Is this financial advice?
No. This bot is created for educational purposes only.

---

3. Can I make money using this information?
Trading involves risk, and profits are not guaranteed.

---

4. Who is this bot for?
Beginners who want to understand trading step by step.

---

5. Do I need prior experience?
No. Everything is beginner-friendly.

---

6. Do you provide personal support?
No one-on-one trading advice.

---

7. Is there any cost?
Basic content is free.

---

⚠️ Disclaimer:
Trading involves financial risk.

“These are projections and not guarantees.”
"""

support_text = """📩 Support

If you have questions, explore lessons and FAQ first.

This bot is for structured self-learning.

⚠️ Disclaimer:
We do not provide personal trading advice.

“These are projections and not guarantees.”
"""

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

# ===== TYPING =====

def typing(chat_id):
    for _ in range(3):
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

# ===== STEPS =====

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

# ===== FAQ =====

@bot.message_handler(func=lambda m: m.text == "❓ FAQ")
def faq(m):
    typing(m.chat.id)
    bot.send_message(m.chat.id, faq_text)

# ===== SUPPORT =====

@bot.message_handler(func=lambda m: m.text == "📩 Support")
def support(m):
    typing(m.chat.id)
    bot.send_message(m.chat.id, support_text)

# ===== QUIZ =====

def q1(chat_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("A) Act fast", callback_data="q1_a"),
        InlineKeyboardButton("B) Observe the market", callback_data="q1_b"),
        InlineKeyboardButton("C) Follow others", callback_data="q1_c")
    )
    bot.send_message(chat_id, "Question 1:\n\nWhat is the first step?", reply_markup=kb)

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

    if call.data == "q1_b":
        bot.send_message(chat_id, "✅ Correct")
        q2(chat_id)
    else:
        bot.send_message(chat_id, "❌ Correct Answer: Observe the market")
        q2(chat_id)

    if call.data == "q2_c":
        bot.send_message(chat_id, "✅ Correct")
        q3(chat_id)
    elif call.data.startswith("q2"):
        bot.send_message(chat_id, "❌ Correct Answer: Emotions")
        q3(chat_id)

    if call.data == "q3_b":
        bot.send_message(chat_id, "✅ Correct")
    elif call.data.startswith("q3"):
        bot.send_message(chat_id, "❌ Correct Answer: Structured thinking")

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
