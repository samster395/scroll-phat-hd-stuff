# scroll-phat-hd-stuff

Just some things I've made for the [Scroll pHAT HD](https://shop.pimoroni.com/products/scroll-phat-hd).

You will need the [Scroll pHAT HD Libary](https://github.com/pimoroni/scroll-phat-hd) installed.

## clock_date_temp_noti_live.py

clock_date_temp_noti_live.py is basically the clock_date_temp.py script but it runs a web server where if you go to the URL printed in the console (http://localhost:8088 by default) with the variables <code>?type=noti</code> at the end of the URL it will flash NOTI on the Scroll pHAT HD.

There is also support for the actual notification title and text, this could be send to the url using Tasker and AutoNotification from your Android device.

## clock_date_temp_cond_scroll.py

clock_date_temp_cond_scroll.py is basically the clock_date_temp.py script but the actual weather condition (I.e. Rain) is shown as well as the Temperature.

### The rest of the scripts should be self-explanatory. :)