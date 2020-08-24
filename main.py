#!/usr/bin/env python3
import requests
import RPi.GPIO as GPIO
import time


if __name__ == '__main__':

    back_door = 2
    # hardware setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(back_door, GPIO.BOTH, bouncetime=200)  # add rising edge detection on a channel

    rising_edge = False
    falling_edge = False
    start_time = 0
    url = 'https://www.w3schools.com/python/demopage.php'
    myobj = {'somekey': 'somevalue'}

    while True:
        if GPIO.event_detected(back_door):
            # if we're here, an edge was detected
            time.sleep(0.005)  # debounce for 5mSec
            # If input is True is a Rising EDGE else a Falling EDGE
            if GPIO.input(back_door) == 1:
                start_time = time.time()
                rising_edge = True
                falling_edge = False
            else:
                falling_edge = True
                rising_edge = False

        # If The door is Open
        if rising_edge:
            # Count 10 seconds
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:
                #   generate a POST Request to notify that DOOR has been OPENED
                x = requests.post(url, data=myobj)
                # restart the timmer to send other POST request after 10 senconds more
                start_time = time.time()
        if falling_edge:
            # generate a POST Request to notify that DOOR has beed closed
            falling_edge = True
        time.sleep(.01)     # Delay to not use the whole cpu
    # clean all
    GPIO.cleanup()
