import network
import time
import rp2
import ntptime
import machine

from bin import get_all_bins
from bin_display import BinDisplay

rp2.country('GB')

# Edit the file config_sample.py and rename it to config.py

display = BinDisplay()

try:
    import config
except ImportError:
    display.error("Configuration needed")
    exit()


wlan = network.WLAN(network.STA_IF)

while True:
    wlan.active(True)
    wlan.connect(config.WIFI_SSID,  config.WIFI_PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(5)

    if wlan.status() != 3:
        display.error("Could not connect to WiFi")
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

        print(wlan.ifconfig())

        print("Setting time")
        ntptime.settime()

        bins = get_all_bins()

        display.bins(bins)

    wlan.disconnect()
    wlan.active(False)

    print("Sleeping")
    time.sleep(30)  # Short time while testing
    print("Awake")



