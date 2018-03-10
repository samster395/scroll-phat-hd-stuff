from datetime import datetime
import time
import scrollphathd
from scrollphathd.fonts import font3x5
# Brightness of the seconds bar and text
BRIGHTNESS = 0.1
SLPFunc = True # Set this to true if you want the clock to turn the display off between the times set below
SLPtimeStart = '21:59'
SLPtimeEnd = '06:59'

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
    #time.sleep(0.1)
try:	
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
                clock()   
            time.sleep(0.1)
        else:
            clock()
            time.sleep(0.1)
except KeyboardInterrupt:
    print(' Keyboard Interrupt!')
    scrollphathd.clear()
    scrollphathd.show()