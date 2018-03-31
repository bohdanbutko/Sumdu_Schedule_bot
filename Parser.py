import requests
import bs4
import datetime

from Lesson import Lesson


class Parser(object):

    days = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье",
    }

    les_amount = {
        1: "пара.",
        2: "пары.",
        3: "пары.",
        4: "пары.",
        5: "пар.",
        6: "пар.",
        7: "пар.",
        8: "пар."
    }

    def __init__(self):
        self.request_url = "http://schedule.sumdu.edu.ua/index/htmlschedule"
        self.lessons = []

    def send_request(self, group_code):
        params = {
            "data[DATE_BEG]": datetime.datetime.now().strftime("%d.%m.%Y"),
            "data[DATE_END]": datetime.datetime.now().strftime("%d.%m.%Y"),
            "data[KOD_GROUP]": group_code,
            "data[ID_FIO]": 0,
            "data[ID_AUD]": 0,
            "data[PUB_DATE]": "false",
            "data[PARAM]": 0
        }

        response = requests.post(self.request_url, data=params)
        response.encoding = "windows-1251"

        self.__parse_data(response)

    def __parse_data(self, data):
        b = bs4.BeautifulSoup(data.text, "html.parser")
        content = b.select("table tbody tr td")
        self.lessons = []

        for (index, value) in enumerate(content, start=1):
            res = value.select("div")

            if len(res) > 1:
                try:
                    lesson = Lesson()

                    lesson.set_number(index)
                    lesson.set_name(res[0].getText())
                    lesson.set_type(res[1].getText())
                    lesson.set_audience(res[2].getText())
                    lesson.set_professor(res[3].getText())
                    lesson.set_group(res[4].getText())

                    self.lessons.append(lesson)
                except IndexError:
                    pass

    def create_message(self):
        message = "Сегодня {} {}, ".format(
            Parser.days[datetime.datetime.now().strftime("%A")],
            datetime.datetime.now().strftime("%d.%m"))

        if len(self.lessons) > 0:
            message += "у тебя {} {}".format(
                len(self.lessons),
                Parser.les_amount[len(self.lessons)])

            for les in self.lessons:
                message += "\n\n"
                message += str(les)
        else:
            message += "у тебя нет пар."

        return message
