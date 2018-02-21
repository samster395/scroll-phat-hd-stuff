import threading
import time
import os
from gpiozero import Button
import scrollphathd
from scrollphathd.fonts import font3x5
import json
import httplib2 # Do 'pip install httplib2' - Used to cache the data - https://github.com/httplib2/httplib2
h = httplib2.Http("/home/pi/clock/cache") # Edit this path accordingly,  it would be a good idea to make this a tmpfs folder to extend the life of your sd card

button = Button(17)
button2 = Button(27)
pressed = 0

pid = os.getpid()
print("Current Task PID: " + str(pid) + ", Use command 'kill -9 " + str(pid) + "' from another console if you need to end this script")

BRIGHTNESS = 0.1 # Brightness of the display, I would suggest not putting it to full(1.0), it is very bright
CITY_ID = "" # Find your city here http://openweathermap.org/ and copy the city id from the URL looking like this http://openweathermap.org/city/2643743
OPENWEATHER_APIKEY = "" # Get your API Key here http://openweathermap.org/appid
UNITS = "metric" # metric or imperial
CACHE_TIME = "1800" # How long to cache the temp data in seconds, default is 30 minutes

def clock():
    scrollphathd.clear()
    scrollphathd.write_string(time.strftime("%H:%M"), x=0, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.show()
    time.sleep(1)
	
def date():
    scrollphathd.clear()
    scrollphathd.write_string(time.strftime("%d"), x=0, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.fill(BRIGHTNESS, x=8, y=0, width=1, height=7)
    scrollphathd.write_string(time.strftime("%m"), x=10, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.show()
	
def temp():
	scrollphathd.clear()
	(resp_headers, content) = h.request("http://api.openweathermap.org/data/2.5/weather?id=" + CITY_ID + "&appid=" + OPENWEATHER_APIKEY + "&units=" + UNITS, "GET", headers={'cache-control':'max-age=' + CACHE_TIME})
	data = json.loads(content.decode('utf-8'))
	t = str(data['main']['temp'])
	tt = float(t)
	if UNITS == "imperial" :
	    TF = "F"
	else :
	    TF = "C"
	string = "%.1f" % tt + TF
	scrollphathd.write_string(string, x=0, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
	scrollphathd.show()

def ButtonDectector():
    while True:
        if button.is_pressed:
            global BRIGHTNESS
            global pressed
            pressed += 1
            if pressed == 1:
                BRIGHTNESS = 0.5
                print("Setting Brightness to 0.5, brightness will update within 30 seconds")
            elif pressed == 2:
                BRIGHTNESS = 1.0
                print("Setting Brightness to 1.0, brightness will update within 30 seconds")
            elif pressed == 3:
                BRIGHTNESS = 0.1
                print("Setting Brightness to 0.1, brightness will update within 30 seconds")
                pressed = 0
            time.sleep(1)

        elif button2.is_pressed:
            print("Button 2 pressed, Powering off system")
            os.system("sudo poweroff")
            time.sleep(1)

def ClockLoop():
    while True:
        clock()
        time.sleep(30)
        date()
        time.sleep(5)
        temp()
        time.sleep(5)

# Because of the way this works, it cant be killed with control-c, you'll have to kill it with the PID
thread1 = threading.Thread(target=ButtonDectector)
thread1.start()

thread2 = threading.Thread(target=ClockLoop)
thread2.start()