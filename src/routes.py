from flask import Flask
from rai import RaiParser
from telegram import TelegramParser

app = Flask(__name__)


@app.route("/rai_play_sound/<slug>")
def get_feed(slug):
    rai_parser = RaiParser(slug)
    return rai_parser(), 200, {"Content-Type": "application/rss+xml"}


@app.route("/telegram/<channel_id>")
def get_telegram_feed(channel_id):
    tgp = TelegramParser(channel_id)
    return tgp(), 200  # , {"Content-Type": "application/rss+xml"}
