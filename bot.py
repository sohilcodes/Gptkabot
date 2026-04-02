import os
import time
import telebot
import threading
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not found")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ===== USER DATA (simple memory) =====
users = {}

# ===== TEXT =====

disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this.
"""

welcome = """This is not a signal service.

It’s a learning environment to help you understand markets step by step.

Start below.
"""

market = """📈 Market Structure

Markets move in phases:

• Uptrend
• Downtrend
• Range

Recognizing structure avoids random decisions.
"""

psychology = """🧠 Trading Psychology

Most mistakes come from emotions:

• Fear
• Overconfidence
• Impatience

Control emotions = better decisions.
"""

risk = """⚖️ Risk Awareness

• Never over-risk
• Protect capital
• Stay disciplined

Risk control keeps you alive.
"""

decision = """⚙️ Decision Framework

Before acting:

• What is the condition?
• Is risk defined?
• Am I following a plan?

Structure reduces mistakes.
"""

final_text = """You’ve completed the basics.

Most people stop here.

If you want to go deeper:

@your_username
"""

# ===== MENU =====

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📈 Market Structure", "🧠 Trading Psychology")
    kb.row("⚖️ Risk Awareness", "⚙️ Decision Framework")
    return kb


# ===== FINAL DELAY MESSAGE =====

def send_final(chat_id):
    time.sleep(15)
    bot.send_message(chat_id, final_text)


# ===== START =====

@bot.message_handler(commands=['start'])
def start(msg):

    user_id = msg.from_user.id

    if user_id not in users:
        users[user_id] = {"steps": set(), "done": False}

        d = bot.send_message(msg.chat.id, disclaimer)

        try:
            bot.pin_chat_message(msg.chat.id, d.message_id)
        except:
            pass

    bot.send_message(msg.chat.id, welcome, reply_markup=menu())


# ===== HANDLER FUNCTION =====

def handle_step(msg, text, step_name):
    user_id = msg.from_user.id

    bot.send_message(msg.chat.id, "Thinking...")
    time.sleep(2)

    bot.send_message(msg.chat.id, text)

    users[user_id]["steps"].add(step_name)

    # Check completion
    if len(users[user_id]["steps"]) == 4 and not users[user_id]["done"]:
        users[user_id]["done"] = True
        threading.Thread(target=send_final, args=(msg.chat.id,)).start()


# ===== BUTTONS =====

@bot.message_handler(func=lambda m: m.text == "📈 Market Structure")
def b1(m):
    handle_step(m, market, "market")

@bot.message_handler(func=lambda m: m.text == "🧠 Trading Psychology")
def b2(m):
    handle_step(m, psychology, "psychology")

@bot.message_handler(func=lambda m: m.text == "⚖️ Risk Awareness")
def b3(m):
    handle_step(m, risk, "risk")

@bot.message_handler(func=lambda m: m.text == "⚙️ Decision Framework")
def b4(m):
    handle_step(m, decision, "decision")


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
