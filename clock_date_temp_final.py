import time	#returns time values
import scrollphathd
from scrollphathd.fonts import font5x5
from scrollphathd.fonts import font3x5
import json
import httplib2 # Do 'pip install httplib2' - Used to cache the data - https://github.com/httplib2/httplib2
h = httplib2.Http(".cache")

# Display a progress bar for seconds
# Displays a dot if False
DISPLAY_BAR = False

# Brightness of the seconds bar and text
BRIGHTNESS = 0.1

CITY_ID = "" # Find your city here http://openweathermap.org/ and copy the city id from the URL looking like this http://openweathermap.org/city/2643743

OPENWEATHER_APIKEY = "" # Get your API Key here http://openweathermap.org/appid

UNITS = "metric"

def clock():
    #print("clock")
    scrollphathd.clear()
    # Grab the "seconds" component of the current time
    # and convert it to a range from 0.0 to 1.0
    float_sec = (time.time() % 60) / 59.0

    # Multiply our range by 15 to spread the current
    # number of seconds over 15 pixels.
    #
    # 60 is evenly divisible by 15, so that
    # each fully lit pixel represents 4 seconds.
    #
    # For example this is 28 seconds:
    # [x][x][x][x][x][x][x][ ][ ][ ][ ][ ][ ][ ][ ]
    #  ^ - 0 seconds                59 seconds - ^
    seconds_progress = float_sec * 15

#    if DISPLAY_BAR:
#        # Step through 15 pixels to draw the seconds bar
#        for y in range(15):
#            # For each pixel, we figure out its brightness by
#            # seeing how much of "seconds_progress" is left to draw
#            # If it's greater than 1 (full brightness) then we just display 1.
#            current_pixel = min(seconds_progress, 1)
#
#            # Multiply the pixel brightness (0.0 to 1.0) by our global brightness value
#            scrollphathd.set_pixel(y + 1, 6, current_pixel * BRIGHTNESS)
#
#            # Subtract 1 now we've drawn that pixel
#            seconds_progress -= 1
#
#            # If we reach or pass 0, there are no more pixels left to draw
#            if seconds_progress <= 0:
#                break
#
#    else:
#        # Just display a simple dot
#        scrollphathd.set_pixel(int(seconds_progress), 6, BRIGHTNESS)

    # Display the time (HH:MM) in a 5x5 pixel font
    scrollphathd.write_string(
        time.strftime("%H:%M"),
        x=0, # Align to the left of the buffer
        y=1, # Align to the top of the buffer
        font=font5x5, # Use the font5x5 font we imported above
        brightness=BRIGHTNESS # Use our global brightness value
    )

    # int(time.time()) % 2 will tick between 0 and 1 every second.
    # We can use this fact to clear the ":" and cause it to blink on/off
    # every other second, like a digital clock.
    # To do this we clear a rectangle 8 pixels along, 0 down,
    # that's 1 pixel wide and 5 pixels tall.
    #if int(time.time()) % 2 == 0:
    #    scrollphathd.clear_rect(8, 0, 1, 5)

    # Display our time and sleep a bit. Using 1 second in time.sleep
    # is not recommended, since you might get quite far out of phase
    # with the passing of real wall-time seconds and it'll look weird!
    #
    # 1/10th of a second is accurate enough for a simple clock though :D
    scrollphathd.show()
    time.sleep(0.1)
	
def date():
    scrollphathd.clear()
    scrollphathd.write_string(time.strftime("%d"), x=0, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.set_pixel(8, 3, BRIGHTNESS)
    scrollphathd.write_string(time.strftime("%m"), x=10, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.show()
	
def weather():
	scrollphathd.clear()
	(resp_headers, content) = h.request("http://api.openweathermap.org/data/2.5/weather?id=2640354&appid=4ff22ccfa9e8055c09e9c32eaa96d9cc&units=metric", "GET", headers={'cache-control':'max-age=1800'})
	data = json.loads(content)
	t = str(data['main']['temp'])
	tt = float(t)
	string = "%.1f" % tt + "C"
	scrollphathd.write_string(string, x=0, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
	scrollphathd.show()

try:	
	while True:
		clock()
		time.sleep(30)
		date()
		time.sleep(5)
		weather()
		time.sleep(5)
except KeyboardInterrupt:
    print(' Keyboard Interrupt!')
    scrollphathd.clear()
    scrollphathd.show()