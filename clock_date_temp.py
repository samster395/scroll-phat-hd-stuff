import time	#returns time values
import scrollphathd
from scrollphathd.fonts import font5x5
from scrollphathd.fonts import font3x5
import json
import httplib2 # Do 'pip install httplib2' - Used to cache the data - https://github.com/httplib2/httplib2
h = httplib2.Http(".cache")

BRIGHTNESS = 0.1 # Brightness of the display, I would suggest not putting it to full(1.0), it is very bright
CITY_ID = "" # Find your city here http://openweathermap.org/ and copy the city id from the URL looking like this http://openweathermap.org/city/2643743
OPENWEATHER_APIKEY = "" # Get your API Key here http://openweathermap.org/appid
UNITS = "metric" # metric or imperial
CACHE_TIME = "1800" # How long to cache the temp data in seconds, default is 30 minutes

def clock():
    scrollphathd.clear()
    scrollphathd.write_string(time.strftime("%H:%M"), x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.show()
	
def date():
    scrollphathd.clear()
    scrollphathd.write_string(time.strftime("%d"), x=0, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.set_pixel(8, 3, BRIGHTNESS)
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

try:	
	while True:
		clock()
		time.sleep(30)
		date()
		time.sleep(5)
		temp()
		time.sleep(5)
except KeyboardInterrupt:
    print(' Keyboard Interrupt!')
    scrollphathd.clear()
    scrollphathd.show()