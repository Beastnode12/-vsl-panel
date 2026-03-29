import telebot
from flask import Flask, request, jsonify
import json, os, threading

# 🔐 PUT YOUR TOKEN HERE (TEMP METHOD)
BOT_TOKEN = "7843555823:AAGXZL7kwL1Q7o0hrH7gDgINk2KTi5Nymjc"

bot = telebot.TeleBot(7843555823:AAGXZL7kwL1Q7o0hrH7gDgINk2KTi5Nymjc)
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

# START COMMAND
@bot.message_handler(commands=['start'])
def start(msg):
    user_id = str(msg.from_user.id)
    data = load_db()

    if user_id not in data:
        data[user_id] = {
            "name": msg.from_user.first_name,
            "bots": [],
            "channels": []
        }
        save_db(data)

    bot.send_message(msg.chat.id, "🔥 VSL PRIME PANEL CONNECTED")

# HOME
@app.route("/")
def home():
    return "VSL ENGINE RUNNING 🔥"

# GET USER DATA
@app.route("/get/<user>")
def get_user(user):
    data = load_db()
    return jsonify(data.get(user, {}))

# ADD BOT
@app.route("/add_bot", methods=["POST"])
def add_bot():
    req = request.json
    data = load_db()

    user = str(req["user"])
    botname = req["bot"]

    if user in data:
        data[user]["bots"].append(botname)

    save_db(data)
    return {"status": "ok"}

# ADD CHANNEL
@app.route("/add_channel", methods=["POST"])
def add_channel():
    req = request.json
    data = load_db()

    user = str(req["user"])
    channel = req["channel"]

    if user in data:
        data[user]["channels"].append(channel)

    save_db(data)
    return {"status": "ok"}

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

# RUN BOTH
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=8080)
