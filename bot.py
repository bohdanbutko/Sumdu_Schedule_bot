from telegram.ext import Updater, CommandHandler
from config import TOKEN
from config import GROUPS
from Parser import Parser

import logging
import telebot
import json


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
schedule_parser = Parser()
bot = telebot.TeleBot(TOKEN)
users = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


def set_group(bot, updater):
    chat_id = updater.message.chat.id
    try:
        group = updater.message.text.split(" ")[1]
        users[chat_id] = GROUPS[group]

        with open("users.json", "w") as users_file:
            json.dump(users, users_file)

        bot.send_message(chat_id, "Группа установлена")
    except KeyError:
        bot.send_message(chat_id, "Группа не найдена")
    except IndexError:
        bot.send_message(chat_id, "Необходимо указать группу\n" +
                         "Например: /set_group ІН.м.н-71")


def schedule(bot, updater):
    chat_id = updater.message.chat.id

    with open("users.json") as users_file:
        try:
            chats = json.load(users_file)
            group_code = chats[str(chat_id)]
            schedule_parser.send_request(group_code)
            text = schedule_parser.create_message()
            bot.send_message(chat_id, text)
        except:
            text = "Необходимо задать группу"
            bot.send_message(chat_id, text)


def my_group(bot, updater):
    chat_id = updater.message.chat.id
    group_code = None

    with open("users.json") as users_file:
        chats = json.load(users_file)
        group_code = chats[str(chat_id)]

    for (group, code) in GROUPS.items():
        if code == group_code:
            bot.send_message(chat_id, group)


my_group_handler = CommandHandler("my_group", my_group)
schedule_handler = CommandHandler("schedule", schedule)
set_group_handler = CommandHandler("set_group", set_group)
dispatcher.add_handler(set_group_handler)
dispatcher.add_handler(schedule_handler)
dispatcher.add_handler(my_group_handler)


def send_schedule():

    with open("users.json") as users_file:
        chats = json.load(users_file)

        for chat in chats:
            group = chats[chat]
            schedule_parser.send_request(group)
            text = schedule_parser.create_message()
            bot.send_message(chat, text)


if __name__ == "__main__":
    try:
        updater.start_polling()
    except KeyboardInterrupt:
        exit()
