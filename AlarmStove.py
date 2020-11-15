#!/usr/bin/env python3

#GEHMERT JC - 14 nov 2020 - Get pellet level
#Max distance 66cm, alarm for 55cm , full for 3cm

import RPi.GPIO as GPIO
import time

print ("+-----------------------------------------------------------+")
print ("|   Natalya OS by Gehhack - Mesure Ultrason                 |")
print ("|   Get level pellet                                        |")
print ("+-----------------------------------------------------------+")

alarm_pellet = 0

def GetDistance():
    global alarm_pellet
    stove_pelletlevel = "/home/pi/Scripts/out/pellet_level.res"
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pin_trigger = 23
    pin_echo = 24
    GPIO.setup(pin_trigger,GPIO.OUT)
    GPIO.setup(pin_echo,GPIO.IN)
    GPIO.output(pin_trigger, False)
    time.sleep(0.5)
    GPIO.output(pin_trigger, True)
    time.sleep(0.00001)
    GPIO.output(pin_trigger, False)
    while GPIO.input(pin_echo)==0:
        pulse_start = time.time()

    while GPIO.input(pin_echo)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17165
    distance = round(distance, 1) 
    GPIO.cleanup()
    min = 0
    max = 100
    #pellet = 100 - distance #* 0.3
    print (distance)

    #Alarm trigger
    if distance > 55:
        alarm_pellet = 1

    if distance < max and distance > min:
        fichier = open(stove_pelletlevel, "w")
        fichier.write(str(distance))
        fichier.close()
    else:
        fichier = open(stove_pelletlevel, "w")
        fichier.write("error")
        fichier.close()

def LedAlarmPellet():
    print (alarm_pellet)
    pin_led = 17
    led_on = GPIO.HIGH
    led_off = GPIO.LOW
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin_led,GPIO.OUT)
    if (alarm_pellet) > 0:
        print("Alarm pellet")
        GPIO.output(pin_led,led_on)
        time.sleep(1)
    else:
        print("No alarm pellet, cool")
        GPIO.output(pin_led,led_off)

GetDistance()
LedAlarmPellet()
