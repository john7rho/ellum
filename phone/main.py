from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse, Start, Stream
import boto3
from botocore.exceptions import NoCredentialsError
import os
import requests
import uuid
import sys

app = Flask(__name__)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Set up Amazon Transcribe
    # transcribe = boto3.client('transcribe')
    transcribe = boto3.client('transcribe', aws_access_key_id='AKIASYSAF2CEXXUGTFFP',
                              aws_secret_access_key='IUb/4wgC/l8vfnFBbd1nmFMYQE3pf4R5gcHYnWWD', region_name='us-west-2')
    # job_name = str(uuid.uuid4())
    # media_format = 'audio/wav'
    # media_sample_rate_hz = 8000
    # language_code = 'en-US'

    # Set up Twilio
    response = VoiceResponse()
    gather = Gather(input='speech', action='/completed')
    # gather = Gather(action='/transcribe', method='POST')
    # gather.say('Welcome to Twilio, please tell us why you\'re calling')
    # response.record(play_beep=True, max_duration=120)
    # response.append(gather)
    # print(response, file=sys.stderr)
    return str(response)
    # response.record(
    #     timeout=5,
    #     action='/upload',
    #     method='POST',
    #     # transcribe='true',
    # )

    # Get audio data from Twilio
    #print(request.form.get, file=sys.stderr)
    # audio_url = request.form['RecordingUrl']
    # recording_url = requests.form.get('RecordingUrl')
    # print('recording_url: ' + audio_url, file=sys.stderr)
    # audio_data = requests.get(audio_url).content
    # audio_data = requests.get(recording_url).content

    # Start Amazon Transcribe job
    # transcribe.start_stream_transcription(
    #     LanguageCode=language_code,
    #     MediaFormat=media_format,
    #     MediaSampleRateHertz=media_sample_rate_hz,
    #     AudioStream={
    #         'AudioEvent': {
    #             'AudioChunk': audio_data
    #         }
    #     },
    #     TranscriptionJobName=job_name,
    # )

    # print(response)
    # return str(response)


# @app.route('/voice', methods=['POST'])
# def voice():
#     print('working!')
#     response = VoiceResponse()
#     response.say(
#         'Hello, welcome to the Ellum support line. What is your question?')
#     response.record(
#         timeout=5,
#         action='/upload',
#         method='POST',
#         transcribe='true',
#     )
#     # start = Start()
#     # start.stream(
#     #     name='Example Audio Stream', url='wss://mystream.ngrok.io/audiostream'
#     # )
#     # response.append(start)
#     return str(response)


# @app.route('/upload', methods=['POST'])
# def upload():
#     recording_url = request.form.get('RecordingUrl')
#     if recording_url:
#         upload_to_s3(recording_url)
#     return 'OK'


# def upload_to_s3(recording_url):
#     # s3 = boto3.client('s3')
#     s3 = boto3.client('s3', aws_access_key_id='AKIASYSAF2CEXXUGTFFP',
#                       aws_secret_access_key='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', region_name='us-west-2')
#     bucket_name = 'ellumtreehacks'
#     file_name = f'{os.urandom(16).hex()}.wav'
#     response = requests.get(recording_url)
#     s3.put_object(Bucket=bucket_name, Key=file_name, Body=response.content)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port='5001')
