import telebot
from flask import Flask, request, jsonify
import json
import os

BOT_TOKEN = "YOUR_PANEL_BOT_TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

DB_FILE = "data.json"

# CREATE DB
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE) as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# START
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    data = load_db()

    if user_id not in data:
        data[user_id] = {
            "name": message.from_user.first_name,
            "bots": [],
            "channels": []
        }
        save_db(data)

    bot.send_message(message.chat.id, "🔥 VSL PRIME PANEL READY")

# ADD BOT
@app.route("/add_bot", methods=["POST"])
def add_bot():
    data = load_db()
    req = request.json

    user = str(req["user"])
    botname = req["bot"]

    data[user]["bots"].append(botname)
    save_db(data)

    return jsonify({"status":"ok"})

# ADD CHANNEL
@app.route("/add_channel", methods=["POST"])
def add_channel():
    data = load_db()
    req = request.json

    user = str(req["user"])
    channel = req["channel"]

    data[user]["channels"].append(channel)
    save_db(data)

    return jsonify({"status":"ok"})

# GET DATA
@app.route("/get_data/<user>")
def get_data(user):
    data = load_db()
    return jsonify(data.get(user, {}))

# GLOBAL STATS
@app.route("/stats")
def stats():
    data = load_db()

    total_users = len(data)
    total_bots = sum(len(u["bots"]) for u in data.values())
    total_channels = sum(len(u["channels"]) for u in data.values())

    return jsonify({
        "users": total_users,
        "bots": total_bots,
        "channels": total_channels
    })

# RUN
if __name__ == "__main__":
    bot.infinity_polling()
