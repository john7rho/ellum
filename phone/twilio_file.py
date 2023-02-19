from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from twilio.jwt.access_token import AccessToken
import requests
import json
import time

# set up your Twilio account credentials
# account_sid = 'SKd3da78bbd73bc5333c6c82cfbcf7d4f9'
account_sid = 'ACb0a867ab740491949b844e83a1c1d5ed'
auth_token = '1f58ce7a661165c40b78be4f28139e86'
# auth_token = 'af28bc979c925c001a2118e1b99a5a12'
api_secret = '9zgQhDI7tmXQ1TevBSNWsoum5xKbOug4'

# set up a Twilio client
client = Client(account_sid, auth_token)
# generate a Twilio access token for the Programmable Voice SDK
voice_token = AccessToken(account_sid, auth_token, api_secret, identity='user')

# initiate a call to the phone number using Twilio's Programmable Voice service
call = client.calls.create(
    # a TwiML document that tells Twilio what to do when the call is answered
    url='http://demo.twilio.com/docs/voice.xml',
    to='+14698038888',  # the phone number to call
    from_='+18663227747'  # your Twilio phone number
)
call_sid = call.sid
print(f"Call initiated with SID {call_sid}.")

# wait for the call to be connected and transcribing
while True:
    call = client.calls(call_sid).fetch()
    call_status = call.status
    if call_status in ['in-progress', 'completed']:
        transcription_status = call.media.transcription.status
        if transcription_status == 'in-progress':
            transcript = call.media.transcription.transcription_text
            print(f"Transcription in progress: {transcript}")
            break
    time.sleep(5)

# continuously monitor the transcription and reply to the caller based on the transcribed text
while True:
    call = client.calls(call_sid).fetch()
    transcription_status = call.media.transcription.status
    if transcription_status == 'completed':
        transcript = call.media.transcription.transcription_text
        print(f"Transcription completed: {transcript}")
        if 'hello' in transcript.lower():
            reply = VoiceResponse()
            reply.say("Hello, how can I help you?")
            response_xml = str(reply)
            client.calls(call_sid).update(twiml=response_xml)
        elif 'goodbye' in transcript.lower():
            reply = VoiceResponse()
            reply.say("Goodbye!")
            response_xml = str(reply)
            client.calls(call_sid).update(twiml=response_xml)
            break
    elif transcription_status == 'in-progress':
        transcript = call.media.transcription.transcription_text
        print(f"Transcription in progress: {transcript}")
    time.sleep(5)
