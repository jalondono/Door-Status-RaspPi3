#!/usr/bin/env python3
import requests
import RPi.GPIO as GPIO
import time


def telegram_message(warning: str):
    BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format("...")
    TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'.format(1192866213, warning)
    requests.post(TELEGRAM_SEND_MESSAGE_URL)


if __name__ == '__main__':

    back_door = 8
    # hardware setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(back_door, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(back_door, GPIO.BOTH, bouncetime=200)  # add rising edge detection on a channel

    rising_edge = False
    falling_edge = False
    start_time = 0

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
            if elapsed_time > 1:
                #   generate a POST Request to notify that DOOR has been OPENED
                telegram_message("Warning: Your door is open")
                # restart the timmer to send other POST request after 10 senconds more
                start_time = time.time()
                print('interrupt')
        if falling_edge:
            # generate a POST Request to notify that DOOR has beed closed
            falling_edge = True
        time.sleep(.01)     # Delay to not use the whole cpu
    # clean all
    GPIO.cleanup()
