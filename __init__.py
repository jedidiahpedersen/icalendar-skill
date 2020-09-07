from mycroft import MycroftSkill, intent_file_handler


class Icalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('icalendar.intent')
    def handle_icalendar(self, message):
        self.speak_dialog('icalendar')


def create_skill():
    return Icalendar()

