import time
from datetime import datetime
import threading
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import cgi
import scrollphathd
from scrollphathd.fonts import font3x5
from scrollphathd.fonts import font5x5
import json
import httplib2 # Do 'pip install httplib2' - Used to cache the data - https://github.com/httplib2/httplib2
h = httplib2.Http("/home/pi/clock/cache") # Edit this path accordingly,  it would be a good idea to make this a tmpfs folder to extend the life of your sd card
exitl1 = False

BRIGHTNESS = 0.1 # Brightness of the display, I would suggest not putting it to full(1.0), it is very bright
CITY_ID = "" # Find your city here http://openweathermap.org/ and copy the city id from the URL looking like this http://openweathermap.org/city/2643743
OPENWEATHER_APIKEY = "" # Get your API Key here http://openweathermap.org/appid
UNITS = "metric" # metric or imperial
CACHE_TIME = "1800" # How long to cache the temp data in seconds, default is 30 minutes
SLPFunc = True # Set this to true if you want the clock to turn the display off between the times set below
SLPtimeStart = '21:59'
SLPtimeEnd = '06:59'

pid = os.getpid()
print("Current Task PID: " + str(pid) + ", Use command 'kill -9 " + str(pid) + "' from another console if you need to end this script")

SLPtimeStart = datetime.strptime(SLPtimeStart, "%H:%M")
SLPtimeEnd = datetime.strptime(SLPtimeEnd, "%H:%M")

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime
        
def clock():
    scrollphathd.clear()
    scrollphathd.write_string(time.strftime("%H:%M"), x=0, y=1, font=font3x5, letter_spacing=1, brightness=BRIGHTNESS)
    scrollphathd.show()
	
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

def loop1():
    while True:
        if exitl1 == True:
            #print("loop 1 has been ended")
            time.sleep(5)
        else:
            if SLPFunc:
                now = datetime.now()
                timeNow = now.strftime("%H:%M")
                timeNow = datetime.strptime(timeNow, "%H:%M")
                if isNowInTimePeriod(SLPtimeStart, SLPtimeEnd, timeNow):
                    scrollphathd.clear()
                    scrollphathd.show()
                    #time.sleep(120)
                else:
                    clock()
                    time.sleep(30)
                    date()
                    time.sleep(5)
                    temp()
                    time.sleep(5)
            else:        
                clock()
                time.sleep(30)
                date()
                time.sleep(5)
                temp()
                time.sleep(5)

def loop2():
    while True:
            if SLPFunc:
                now = datetime.now()
                timeNow = now.strftime("%H:%M")
                timeNow = datetime.strptime(timeNow, "%H:%M")
                if isNowInTimePeriod(SLPtimeStart, SLPtimeEnd, timeNow):
                    scrollphathd.clear()
                    scrollphathd.show()
                    #time.sleep(120)
                else:
                    class GP(BaseHTTPRequestHandler):
                        def _set_headers(self):
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                        def do_HEAD(self):
                            self._set_headers()
                        def do_GET(self):
                            self._set_headers()
                            #print self.path
                            list = parse_qs(self.path[2:])
                            #print parse_qs(self.path[2:])
                            #type = list.get('type')
                            type = str(list.get('type')).replace("'", "").replace("[", "").replace("]", "")
                            #app = "  " + str(list.get('app')).replace("'", "").replace("[", "").replace("]", "")
                            #ti = "  " + str(list.get('ti')).replace("'", "").replace("[", "").replace("]", "")
                            #mes = "  " + str(list.get('mes')).replace("'", "").replace("[", "").replace("]", "")
                            #when = "  " + str(list.get('when')).replace("'", "").replace("[", "").replace("]", "")
                            #print type
                            global exitl1
                            #print app    
                            #print ti      
                            #print mes		
                            #print when
                            self.wfile.write("<html><body><h1>Get Request Received!</h1></body></html>")
                            if type != 'None' :
                                while True:
                                    exitl1 = True
                                    #print("noti received")
                                    scrollphathd.clear()
                                    scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                    scrollphathd.show()
                                    time.sleep(.800)
                                    scrollphathd.clear()
                                    scrollphathd.show()
                                    time.sleep(.800)
                                    scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                    scrollphathd.show()
                                    time.sleep(.800)
                                    scrollphathd.clear()
                                    scrollphathd.show()
                                    time.sleep(.800)
                                    scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                    scrollphathd.show()
                                    time.sleep(.800)
                                    scrollphathd.clear()
                                    scrollphathd.show()
                                    time.sleep(.800)
                                    scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                    scrollphathd.show()
                                    time.sleep(5)
                                    exitl1 = False
                                    break
                    
                    def run(server_class=HTTPServer, handler_class=GP, port=8088):
                        server_address = ('', port)
                        httpd = server_class(server_address, handler_class)
                        print 'Server running at localhost:8088...'
                        httpd.serve_forever()
                    
                    run()
            else:        
                class GP(BaseHTTPRequestHandler):
                    def _set_headers(self):
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                    def do_HEAD(self):
                        self._set_headers()
                    def do_GET(self):
                        self._set_headers()
                        #print self.path
                        list = parse_qs(self.path[2:])
                        #print parse_qs(self.path[2:])
                        #type = list.get('type')
                        type = str(list.get('type')).replace("'", "").replace("[", "").replace("]", "")
                        #app = "  " + str(list.get('app')).replace("'", "").replace("[", "").replace("]", "")
                        #ti = "  " + str(list.get('ti')).replace("'", "").replace("[", "").replace("]", "")
                        #mes = "  " + str(list.get('mes')).replace("'", "").replace("[", "").replace("]", "")
                        #when = "  " + str(list.get('when')).replace("'", "").replace("[", "").replace("]", "")
                        #print type
                        global exitl1
                        #print app    
                        #print ti      
                        #print mes		
                        #print when
                        self.wfile.write("<html><body><h1>Get Request Received!</h1></body></html>")
                        if type != 'None' :
                            while True:
                                exitl1 = True
                                #print("noti received")
                                scrollphathd.clear()
                                scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                scrollphathd.show()
                                time.sleep(.800)
                                scrollphathd.clear()
                                scrollphathd.show()
                                time.sleep(.800)
                                scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                scrollphathd.show()
                                time.sleep(.800)
                                scrollphathd.clear()
                                scrollphathd.show()
                                time.sleep(.800)
                                scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                scrollphathd.show()
                                time.sleep(.800)
                                scrollphathd.clear()
                                scrollphathd.show()
                                time.sleep(.800)
                                scrollphathd.write_string("NOTI", x=0, y=1, font=font5x5, letter_spacing=1, brightness=BRIGHTNESS)
                                scrollphathd.show()
                                time.sleep(5)
                                exitl1 = False
                                break
                
                def run(server_class=HTTPServer, handler_class=GP, port=8088):
                    server_address = ('', port)
                    httpd = server_class(server_address, handler_class)
                    print 'Server running at localhost:8088...'
                    httpd.serve_forever()
                
                run()
           
thread1 = threading.Thread(target=loop1)
thread1.start()

thread2 = threading.Thread(target=loop2)
thread2.start()