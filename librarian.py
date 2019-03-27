#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
from slackclient import SlackClient

#slack
slack_token = os.environ['SLACK_TOKEN']
slack = SlackClient(slack_token)

#GPIO SETUP
pins_zones = {
        "17" : "zone1",
        "27" : "zone2"
}

GPIO.setmode(GPIO.BCM)
for pin, zone in pins_zones.items():
        print "setup " + zone + " pin"
        GPIO.setup(int(pin), GPIO.IN)

def callback(pin):
        print "sound detected in " + pins_zones[str(pin)]
        slack.api_call(
                "chat.postMessage",
                channel="GH926J2P4",
                text="noise detected in " + pins_zones[str(pin)] + ", please remember library rules"
        )

for pin, zone in pins_zones.items():
        print "add callback to " + zone
        #let us know when pin goes high or low
        GPIO.add_event_detect(int(pin), GPIO.BOTH, bouncetime=300) 
        #assign callback to pin, run on change
        GPIO.add_event_callback(int(pin),callback)

while True:
        time.sleep(1)
        