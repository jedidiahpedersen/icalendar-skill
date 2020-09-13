from icalendar import Calendar, Event, Alarm
from datetime import datetime, date, timedelta
from dateutil import rrule

import pytz
import os
import constant
import glob

class VoiceReminder:
    def __init__(self):
        self.datetime = []
        self.message = ''
        self.voicefilepath = ''
        self.uniquename = ''

    def __init__(self, date, message, name=''):
        self.datetime = date
        self.message = message
        self.name = name

def getRemindersFromFolder(calendar_folder, start_datetime, time_delta):
    calendar_files = glob.glob(calendar_folder + "/*")
    
    reminders = []
    for calendar_file in calendar_files:
        reminders += getRemindersFromPath(calendar_file, start_datetime, time_delta)

    return reminders

def getRemindersFromPath(calendar_path, start_datetime, time_delta):
    print(calendar_path)
    calendar_file = open(calendar_path, 'rb')
    ical_object = Calendar.from_ical(calendar_file.read())
    reminders = getReminders(ical_object, start_datetime, time_delta)
    calendar_file.close()
    return reminders

def getReminders(calendar, start_datetime, timedelta):
    l=[]
    for component in calendar.walk():
        alarms = []
        # Is the component an event?
        if component.name != "VEVENT":
            continue
        # Check if the event has any alarms
        alarms = getAlarms(component)
        if len(alarms) == 0:
            continue
        
        end_check_time = start_datetime + timedelta

        # This component is an event with at lease one alarm.

        for alarm in alarms:
            #alarm_time = component.get('dtstart').dt + alarm.get('trigger').dt
            #rulestring = "DTSTART:" 
            #rulestring += alarm_time.strftime('%Y%m%dT%H%M%S\n') 
            #rulestring += component.get('rrule').to_ical().decode("utf-8") 
            
            recursive_rule = getRRULEString(component.get('dtstart').dt + alarm.get('trigger').dt,
            component.get('rrule').to_ical().decode("utf-8"))

            """exclude_rule = getRRULEString(component.get('dtstart').dt + alarm.get('trigger').dt,
            component.get('rrule').to_ical().decode("utf-8"),
            start_datetime)"""

            rule_set = rrule.rruleset()

            r = rrule.rrulestr(recursive_rule)
            for rule_date in r.between(start_datetime, end_check_time):
                name = component.get("SUMMARY")
                name = name.strip()
                name = name.replace(" ", "")
                name = name.casefold()
                name = name.translate(str.maketrans('', '', string.punctuation))
                l.append(VoiceReminder(rule_date, alarm.get('description'), name))

    return l

def getRRULEString(alarm_time, recursive_rule_text):
    #component, alarm, until):
    #alarm_time = component.get('dtstart').dt + alarm.get('trigger').dt
    rulestring = "DTSTART:" 
    rulestring += alarm_time.strftime('%Y%m%dT%H%M%S\n') 
    #rulestring += component.get('rrule').to_ical().decode("utf-8") 
    rulestring += recursive_rule_text
    #rulestring += ";UNTIL=" + end_time.strftime('%Y%m%dT%H%M%S')
    return rulestring

def getAlarms(event):
    eventlist = []
    
    for nested in event.subcomponents:
        if nested.name == 'VALARM' and nested.get('action') == 'DISPLAY':
            eventlist.append(nested)
    return eventlist

def createVoiceFiles(voice_reminders):
    for reminder in voice_reminders: 
        print(reminder.datetime.strftime('%Y%m%dT%H%M%S') + "; " + reminder.message)

def isActive(event, check_time, check_deltatime):
    event_start_time = event.get('dtstart').dt
    end_check_time = check_time + check_deltatime

    # Check if the event start time falls in our time window.
    if check_time < event_start_time < end_check_time:
        return true
    # Check if there is a recursion rule.
    elif event.get('rrule') == {}:
        return False
    
    """rrule = event.get('rrule')
    freq = rrule.get('freq')[0]
    
    if freq == "DAILY":
        return False
    elif freq == "WEEKLY":
        return False
    elif freq == "MONTHLY":
        return False
    elif freq == "YEARLY":
        return False

    return False
    """

"""today = date.today()
wd = today.weekday()

g = open('marcus.ics', 'rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk():
    if component.name == "VEVENT":
        #print(component.get('summary'))
        #print(component.get('dtstart').dt)
        #print(component.get('dtend').dt)
        #print(component.get('dtstamp').dt)
        #if "VALARM" in component.subcomponents:
         #   print("Hello")
        for nested in component.subcomponents:
            if nested.name == 'VALARM':
                print(component.get('summary'))
                print(component.get('dtstart').dt + nested.get('trigger').dt)
                print(nested.get('description'))
                
l = getReminders(gcal,datetime.now(),timedelta(1))
createVoiceFiles(l)
tz=pytz.timezone('America/Denver')
g.close()
"""

def main():
    reminders = getRemindersFromFolder(constant.ICALENDAR_DIRECTORY,datetime.now(),timedelta(1))
    for r in reminders:
        print(r.message)

    pl = glob.glob('/home/pi/icalendar/' + '*ics')

    for p in pl:
        print(p)

    """for calendar_name in calendar_files:
        print(calendar_name)
        g = open(constants.ICALENDAR_DIRECTORY + "/" + calendar_name, 'rb')
        gcal = Calendar.from_ical(g.read())
        reminders += getReminders(gcal,datetime.now(),timedelta(1))
        g.close()
    
    print("Hello!")
    print(constants.ICALENDAR_DIRECTORY)"""

if __name__ == '__main__':
    main()

