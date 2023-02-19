from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Start, Stream
import boto3
from botocore.exceptions import NoCredentialsError
import os
import requests

app = Flask(__name__)


@app.route('/voice', methods=['POST'])
def voice():
    print('working!')
    response = VoiceResponse()
    response.say(
        'Hello, welcome to the Ellum support line. What is your question?')
    response.record(
        timeout=5,
        action='/upload',
        method='POST'
    )
    return str(response)


@app.route('/upload', methods=['POST'])
def upload():
    recording_url = request.form.get('RecordingUrl')
    if recording_url:
        upload_to_s3(recording_url)
    return 'OK'


def upload_to_s3(recording_url):
    # s3 = boto3.client('s3')
    s3 = boto3.client('s3', aws_access_key_id='AKIASYSAF2CEXXUGTFFP',
                      aws_secret_access_key='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', region_name='us-west-2')
    bucket_name = 'ellumtreehacks'
    file_name = f'{os.urandom(16).hex()}.wav'
    response = requests.get(recording_url)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=response.content)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port='5001')
