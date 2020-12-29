#!/usr/bin/env python3
import requests
import RPi.GPIO as GPIO
import time
import os
from twilio.rest import Client


def create_call(phone_numbers: list = ['3122535580']):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    for phone_number in phone_numbers:
        try:
            call = client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml',
                to=f'+57{phone_number}',
                from_='+12517583596'
            )
        except:
            continue
        print(call.sid)


# id group 496704946


def telegram_message(warning: str):
    BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format("1448184781:AAF8QCnpQN-ZZr8Y_ddVY0sgiPWfF0ZJwrs")
    TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'.format(-496704946,
                                                                                             warning)
    requests.post(TELEGRAM_SEND_MESSAGE_URL)


if __name__ == '__main__':
    phone_numbers = ['3122535580', '3005159763', '3008439889']
    back_door = 8
    # hardware setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(back_door, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(back_door, GPIO.BOTH, bouncetime=200)  # add rising edge detection on a channel

    rising_edge = False
    falling_edge = False
    elapsed_ok = False
    past_status = False
    actual_status = False
    start_time = 0
    channel = GPIO.input(back_door)
    start_frequency_time = 0
    elapsed_frequency_time = 0
    time_notifications = 80
    i = 0

    # Check for the initial status of the door when the program start
    if channel:
        rising_edge = True
        elapsed_ok = True
        try:
            telegram_message("Peligro: La puerta del sotano esta abierta")
            create_call(phone_numbers)
        except:
            pass

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

            # detect the rising trigger on the elapsed time to start the second timer
            actual_status = elapsed_time >= 30
            if past_status != actual_status:
                start_frequency_time = time.time()
                past_status = actual_status

            if actual_status:
                try:
                    elapsed_ok = True
                    elapsed_frequency_time = time.time() - start_frequency_time
                    if time.time() - elapsed_frequency_time <= 1:
                        #   generate a POST Request to notify that DOOR has been OPENED
                        telegram_message("Peligro: La puerta del sotano lleva mas de 30  segundos abierta")
                        # Create a phone call
                        create_call(phone_numbers)
                    else:
                        if i > 100 and channel:
                            falling_edge = True
                        if elapsed_frequency_time >= time_notifications or elapsed_frequency_time == time.time():
                            i += 1
                            start_frequency_time = time.time()
                            #   generate a POST Request to notify that DOOR has been OPENED
                            telegram_message(f"Peligro: La puerta del sotano lleva mas de {i*time_notifications} segundos abierta")
                            # Create a phone call
                            create_call(phone_numbers)
                    # restart the timmer to send other POST request after 10 senconds more
                except:
                    pass

        if falling_edge:
            try:
                if elapsed_ok:
                    # generate a POST Request to notify that DOOR has beed closed
                    start_time = time.time()
                    telegram_message("La puerta ha sido cerrada")
                    elapsed_ok = False
                    i = 0
                falling_edge = False
            except:
                pass
        time.sleep(.01)  # Delay to not use the whole cpu
    # clean all
    GPIO.cleanup()
