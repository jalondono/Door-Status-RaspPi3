#!/usr/bin/env python3
import requests
import RPi.GPIO as GPIO
import time
import os
from twilio.rest import Client


def create_call(phone_number: str = '3122535580'):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to=f'+57{phone_number}',
        from_='+12517583596'
    )
    print(call.sid)
# id group 496704946


def telegram_message(warning: str):
    BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format("1448184781:AAF8QCnpQN-ZZr8Y_ddVY0sgiPWfF0ZJwrs")
    TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'.format(-496704946,
                                                                                             warning)
    requests.post(TELEGRAM_SEND_MESSAGE_URL)


if __name__ == '__main__':

    back_door = 8
    # hardware setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(back_door, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(back_door, GPIO.BOTH, bouncetime=200)  # add rising edge detection on a channel

    rising_edge = False
    falling_edge = False
    elapsed_ok = False
    start_time = 0
    channel = GPIO.input(back_door)
    
    # Check for the initial status of the door when the program start
    if channel:
        telegram_message("Peligro: La puerta del sotano esta abierta")
        create_call('3122535580')
        rising_edge = True
        elapsed_ok = True
    
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
            print(f'elapsed_time is: {elapsed_time}')
            if elapsed_time >= 200:
                #   generate a POST Request to notify that DOOR has been OPENED
                telegram_message("Peligro: La puerta del sotano esta abierta")
                # Create a phone call
                create_call('3122535580')
                # restart the timmer to send other POST request after 10 senconds more
                start_time = time.time()
                elapsed_ok = True

        if falling_edge:
            if elapsed_ok:
            # generate a POST Request to notify that DOOR has beed closed
                telegram_message("La puerta ha sido cerrada")
                elapsed_ok = False
            falling_edge = False
        time.sleep(.01)  # Delay to not use the whole cpu
    # clean all
    GPIO.cleanup()
