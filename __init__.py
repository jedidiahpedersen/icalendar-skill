from mycroft import MycroftSkill, intent_file_handler

import sys
sys.path.insert(1, '/opt/mycroft/skills/icalendar-skill')
from loadcalendar import loadcalendar

import os
import constant
from datetime import datetime, timedelta



class Icalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.calendar_refresh_interval = constant.CALENDAR_REFRESH_INTERVAL
        self.calendar_system_folder = constant.ICALENDAR_DIRECTORY

    @intent_file_handler('icalendar.intent')
    def handle_icalendar(self, message):
        self.speak_dialog('icalendar')

    def initialize(self):
        my_setting = self.settings.get('my_setting')
        
        #self.calendar_paths = []
        #TODO include calendar locations from settings
        
        #self.work()
                       
        #self.log.debug(calendar_files)

    def work(self):
        #TODO schedule the schedule_reminders to run every set timedelta.
        self.log.info("Scheduling work to occure again in an interval in seconds.")
        self.schedule_event(self.work,constant.CALENDAR_REFRESH_INTERVAL)
        self.speak("I am doing work and will work again in " + str(constant.CALENDAR_REFRESH_INTERVAL) + " seconds.")

        #TODO schedule the reminders to be said.
        self.schedule_reminders()


    def schedule_reminders(self):
        self.log.info("Loading reminders.")
        reminders = loadcalendar.getRemindersFromFolder(self.calendar_system_folder,
        datetime.now(),timedelta(1))

        for reminder in reminders:
            event = self.schedule_event(self.speak_reminder, reminder.datetime, name=reminder.uniquename)
            self.log.info(event)

    def speak_reminder(self):
        self.log.info("Speaking.")
        self.speak("Speaking.")


def create_skill():
    return Icalendar()

