class Lesson(object):

    time = {
        1: "08:15-09:35",
        2: "09:50-11:10",
        3: "11:25-12:45",
        4: "13:25-14:45",
        5: "15:00-16:20",
        6: "16:35-17:55",
        7: "18:00-19:20",
        8: "19:25-20:45",
    }

    def __init__(self):
        self.number = None
        self.name = None
        self.lesson_type = None
        self.audience = None
        self.professor = None
        self.group = None
        self.time = None

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_type(self):
        return self.lesson_type

    def set_type(self, lesson_type):
        self.lesson_type = lesson_type

    def get_audience(self):
        return self.audience

    def set_audience(self, audience):
        self.audience = audience

    def get_professor(self):
        return self.professor

    def set_professor(self, professor):
        self.professor = professor

    def get_group(self):
        return self.group

    def set_group(self, group):
        self.group = group

    def get_time(self):
        return Lesson.time[self.number]

    def set_time(self, time):
        self.time = time

    def __str__(self):
        return("{}-я пара ({}):\n{} ({}),\nв аудитории {},\nпреподаватель: {}"
               .format(self.get_number(),
                       self.get_time(),
                       self.get_name(),
                       self.get_type(),
                       self.get_audience(),
                       self.get_professor()))
