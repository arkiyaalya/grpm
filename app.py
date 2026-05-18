# This file is kept for reference only.
# The bot is started via: python3 -m FallenRobot (see Procfile)
# Flask health-check is embedded directly in FallenRobot/__main__.py

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return "Bot is alive! 🤖"


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200
