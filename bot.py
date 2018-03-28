from telegram.ext import Updater, CommandHandler
from config import TOKEN
from config import GROUPS
from Parser import Parser

import logging
import telebot


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
schedule_parser = Parser()
bot = telebot.TeleBot(TOKEN)
chat_id = 282498880
users = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


def set_group(bot, updater):
    chat_id = updater.message.chat.id
    group = updater.message.text.split(" ")[1]
    users[chat_id] = GROUPS[group]

    bot.send_message(chat_id, users[chat_id])


set_group_handler = CommandHandler("set_group", set_group)
dispatcher.add_handler(set_group_handler)


def send_schedule():
    parser = schedule_parser
    b = bot

    if parser:
        parser.send_request(1000010)
    else:
        parser = Parser()
        parser.send_request(1000010)

    if b:
        text = parser.create_message()
        b.send_message(chat_id, text)
    else:
        b = telebot.TeleBot(TOKEN)
        text = parser.create_message()
        b.send_message(chat_id, text)


if __name__ == "__main__":
    try:
        updater.start_polling()
    except KeyboardInterrupt:
        exit()
