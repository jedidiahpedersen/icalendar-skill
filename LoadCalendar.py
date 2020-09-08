import sys
sys.path.insert(1, '/home/jedidiah/Projects/LoadCalendar/mycroft-core/mycroft/skills/mycroft_skill/')
#import mycroft_skill

from icalendar import Calendar, Event, Alarm
from datetime import datetime, date, timedelta
from dateutil import rrule

import pytz

class VoiceReminder:
    def __init__(self):
        self.date = []
        self.message = ''
        self.voicefilepath = ''

    def __init__(self, date, message):
        self.date = date
        self.message = message

def getReminders(calendar, start_date, timedelta):
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
        
        end_check_time = start_date + timedelta

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
            start_date)"""

            rule_set = rrule.rruleset()

            r = rrule.rrulestr(recursive_rule)
            for rule_date in r.between(start_date, end_check_time):
                l.append(VoiceReminder(rule_date,alarm.get('description')))

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
        print(reminder.date.strftime('%Y%m%dT%H%M%S') + "; " + reminder.message)

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

today = date.today()
wd = today.weekday()

g = open('marcus.ics', 'rb')
gcal = Calendar.from_ical(g.read())
"""for component in gcal.walk():
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
"""                
l = getReminders(gcal,datetime.now(),timedelta(1))
createVoiceFiles(l)
"""tz=pytz.timezone('America/Denver')"""
g.close()

