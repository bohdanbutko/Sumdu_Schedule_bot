from config import TOKEN
from config import GROUPS
from Parser import Parser

import telebot
import json

schedule_parser = Parser()
bot = telebot.TeleBot(TOKEN)
users = {}


@bot.message_handler(commands=["schedule"])
def schedule(message):
    chat_id = message.chat.id

    with open("users.json") as users_file:
        try:
            chats = json.load(users_file)
            group_code = chats[str(chat_id)]
            schedule_parser.send_request(group_code)
            bot.send_message(chat_id, schedule_parser.create_message())
        except KeyError:
            bot.send_message(chat_id, "Необходимо задать группу.")


@bot.message_handler(commands=["set_group"])
def set_group(message):
    chat_id = message.chat.id
    try:
        group = message.text.split(" ")[1]
        users[chat_id] = GROUPS[group]

        with open("users.json", "w") as users_file:
            json.dump(users, users_file)

        bot.send_message(chat_id, "Группа установлена.")
    except KeyError:
        bot.send_message(chat_id, "Группа не найдена.")
    except IndexError:
        bot.send_message(chat_id, "Необходимо указать группу\n" +
                         "Например: /set_group ІН.м.н-71")


@bot.message_handler(commands=["my_group"])
def my_group(message):
    chat_id = message.chat.id
    try:
        with open("users.json") as users_file:
            chats = json.load(users_file)
            group_code = chats[str(chat_id)]

        for (group, code) in GROUPS.items():
            if code == group_code:
                bot.send_message(chat_id, group)
    except KeyError:
        bot.send_message(chat_id, "Группа не задана.")


def send_schedule():

    with open("users.json") as users_file:
        chats = json.load(users_file)

        for chat in chats:
            group = chats[chat]
            schedule_parser.send_request(group)
            bot.send_message(chat, schedule_parser.create_message())


if __name__ == "__main__":
    try:
        bot.polling()
    except KeyboardInterrupt:
        exit()
