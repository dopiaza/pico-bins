import network
import time
import rp2
import ntptime
import machine

from bin import get_all_bins
from bin_display import BinDisplay
from logger import Logger
from bin_power_ctrl import BinPowerCtrl

led = machine.Pin("LED", machine.Pin.OUT)
led.value(1)

rp2.country('GB')

display = BinDisplay()
logger = Logger()

# Edit the file config_sample.py and rename it to config.py
try:
    import config
except ImportError:
    display.error("Configuration needed")
    exit()



while True:
    led.value(1)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.WIFI_SSID,  config.WIFI_PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        logger.log('Waiting for connection...')
        time.sleep(5)

    if wlan.status() != 3:
        display.error("Could not connect to WiFi")
    else:
        logger.log('connected')
        status = wlan.ifconfig()
        logger.log('ip = ' + status[0])

        logger.log(wlan.ifconfig())

        logger.log("Setting time")
        ntptime.settime()

        bins = get_all_bins()

        display.bins(bins)
        #display.error("Timestamp")

    led.value(0)
    wlan.disconnect()
    wlan.active(False)
    wlan.deinit()

    logger.log("Sleeping")
    pwr = BinPowerCtrl()
    time.sleep_ms(600000)  # 10 minutes, so we can test easily
    pwr.restore()
    logger.log("Awake")



