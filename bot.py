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
CHANNEL = "@task25rs"


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


# ===== TYPING =====

def typing(chat_id):
    for _ in range(5):
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)


# ===== SAFE IMAGE SEND =====

def send_post(chat_id, post_id):
    try:
        bot.copy_message(chat_id, CHANNEL, post_id)
    except:
        bot.forward_message(chat_id, CHANNEL, post_id)


# ===== START =====

@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.from_user.id

    if uid not in users:
        users[uid] = {}

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
    send_post(m.chat.id, 79)


@bot.message_handler(func=lambda m: m.text == "👁 Step 2: Observation")
def step2(m):
    typing(m.chat.id)
    send_post(m.chat.id, 78)


@bot.message_handler(func=lambda m: m.text == "🧠 Step 3: Thinking")
def step3(m):
    typing(m.chat.id)
    send_post(m.chat.id, 77)


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
    kb =
