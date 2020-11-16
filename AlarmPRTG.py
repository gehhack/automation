#!/usr/bin/env python3

#GEHMERT JC - 14 nov 2020 - Alarm PRTG

import os    # standard library
import time
import RPi.GPIO as GPIO
import wget
import os.path
import xml.etree.ElementTree
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

print ("+-----------------------------------------------------------+")
print ("|   Gehhack - Supervision                                   |")
print ("|   Alarm PRTG                                              |")
print ("+-----------------------------------------------------------+")

xmlfile = "/home/pi/Scripts/out/gettreenodestats.xml"
alarm_prtg = 0

def GetXMLfromPRTG():
    url = 'https://172.16.6.110/api/gettreenodestats.xml?username=ro&passhash=4165090358'
    if os.path.exists(xmlfile):
        print('Delete XML from Visor')
        os.remove(xmlfile)
        GetXMLfromPRTG()
    else:
        print('Download XML from Visor')
        wget.download(url, xmlfile)

def ParseXML():
    global alarm_prtg
    tree = xml.etree.ElementTree.parse(xmlfile)
    root = tree.getroot()
    warnsens = root.find('downsens')
    alarm_prtg=int(warnsens.text)
    #Check if the number is int and not str
    #print(type(alarm_prtg))
    print(alarm_prtg)
    
def LedAlarmPRTG():
    pin_led_prtg = 18
    led_on = GPIO.HIGH
    led_off = GPIO.LOW
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin_led_prtg,GPIO.OUT)
    if (alarm_prtg) > 0:
        print("Alarm")
        GPIO.output(pin_led_prtg,led_on)
        time.sleep(1)
    else:
        print("No alarm, cool")
        GPIO.output(pin_led_prtg,led_off)

GetXMLfromPRTG()
ParseXML()
LedAlarmPRTG()
