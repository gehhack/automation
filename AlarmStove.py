#!/usr/bin/env python3

#GEHMERT JC - 14 nov 2020 - Get pellet level
#Max distance 66cm, alarm for 55cm , full for 3cm

import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import math

print ("+-----------------------------------------------------------+")
print ("|   Natalya OS by Gehhack - Mesure Ultrason                 |")
print ("|   Get level pellet                                        |")
print ("+-----------------------------------------------------------+")

alarm_pellet = 0

def GetDistance():
    global alarm_pellet
    global distance
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
    led_off = GPIO.HIGH
    led_on = GPIO.LOW
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
#    GPIO.cleanup()


GetDistance()
LedAlarmPellet()

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
# font = ImageFont.load_default()
# font = ImageFont.truetype('Minecraftia.ttf', 8)


# Police de caracteres /usr/share/fonts/truetype/msttcorefonts
font1 = ImageFont.truetype("arial.ttf",12)    # Definition font1 = arial.ttf
#font2 = ImageFont.truetype("Comic_Sans_MS_Bold.ttf",12)    # Definition font2 = Comic_Sans_MS_Bold.ttf

if distance > 66:
    distance = 66

distanceint = int(distance)
print(distanceint)

mat = [100,100,100,100,99,97,96,94,92,91,89,88,86,84,83,81,80,78,76,75,73,72,70,69,67,65,64,62,61,59,57,56,54,53,51,50,48,46,45,43,42,40,38,37,35,34,32,30,29,27,26,24,23,21,19,18,16,15,13,11,10,8,7,5,3,2,0]
distancecalc = mat[distanceint]



while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    blog = ("Pellet restant :",distancecalc)
    trait =("- - - - - - - - - - - - - - - - -")
    blog1 = ("22 sacs restants")

    # Write two lines of text.
    draw.text((x, top+1), str(blog),  font=font1, fill=255)  # Affichage du texte "blog" avec la police font1
    draw.text((x, top+8), str(trait),  font=font1, fill=255)
    draw.text((x, top+16), str(blog1),  font=font1, fill=255)  # Affichage du texte "blog" avec la police font2
    #draw.text((x, top+25), str(trait),  font=font1, fill=255)


    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
    break
