import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
def create_call(phone_number: str = '3005159763'):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            url='http://demo.twilio.com/docs/voice.xml',
                            to=f'+57{phone_number}',
                            from_='+12517583596'
                        )
    print(call.sid)
