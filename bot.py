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

clarity_text = """🧠 Clarity

Clarity in market learning means having a clear understanding of what is happening and why, instead of reacting to movements without thinking. Many beginners struggle not because markets are complex, but because they try to act without fully understanding the situation.

In simple terms, clarity is the ability to slow down and see the market for what it is, rather than what you expect it to be.

Before taking any action, take a moment to ask yourself:
• What is the price actually doing right now?  
• Am I following a structured and logical approach?  
• Is this decision based on observation or emotion?  

📍 Example:
Imagine you see price suddenly moving upward quickly. Without clarity, a person may react instantly out of excitement or fear of missing out. With clarity, you pause, observe the movement, and try to understand whether this move is stable or temporary. This simple pause can prevent unnecessary mistakes.

Clarity is built over time through observation, patience, and consistent learning. It helps you avoid confusion, reduce emotional reactions, and develop a more disciplined approach to understanding markets.

⚠️ This content is for educational purposes only.  
These are projections and not guarantees.

👉 To continue learning, explore the Observation section.
"""

observation_text = """👀 Observation

Observation is the skill of carefully watching how the market behaves without rushing to take action. It is not just about looking at the chart, but about understanding what the movement is trying to show over time.

Many beginners try to act too quickly, but strong learning comes from watching first and acting later.

When observing, focus on:
• How price moves - fast, slow, or sideways  
• The direction - is it forming an uptrend, downtrend, or no clear trend?  
• Key areas - where price slows down, stops, or changes direction  

📍 Example:
Imagine price is moving upward, but suddenly it starts slowing down near a certain level. Instead of reacting immediately, observation helps you notice that the market is losing momentum. This gives you a better understanding of what might happen next, rather than guessing.

Observation is about patience. The more time you spend watching patterns and behavior, the more familiar the market becomes. Over time, this reduces confusion and helps you make more structured and thoughtful decisions.

Strong observation builds the foundation for clarity and better thinking.

⚠️ This content is for educational purposes only.  
These are projections and not guarantees.

👉 To continue learning, explore the Thinking section.
"""

thinking_text = """💭 Thinking

Thinking in market learning means taking time to understand a situation before acting, instead of reacting instantly. It is the process of analyzing what you see, questioning your decision, and making a calm and structured choice.

Many beginners act quickly based on emotions like excitement, fear, or urgency. Strong thinking helps you slow down and stay in control.

Before making any decision, train yourself to ask:
• What is the reason behind this action?  
• What are the possible outcomes?  
• Am I prepared for both positive and negative situations?  

📍 Example:
Imagine you notice price moving quickly in one direction. Without thinking, a person may react immediately. With proper thinking, you pause and consider: Is this movement stable? Has this happened before? What could happen next? This process reduces unnecessary mistakes.

Thinking also includes planning ahead:
• Understanding your limits  
• Being aware of uncertainty  
• Accepting that not every situation is clear  

Over time, structured thinking helps you become more patient, more disciplined, and less influenced by emotions. It turns reactions into decisions.

⚠️ This content is for educational purposes only.  
These are projections and not guarantees.

👉 To continue learning, explore the Quick Check section.
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
