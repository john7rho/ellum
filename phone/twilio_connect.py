import boto3
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request

app = Flask(__name__)


@app.route('/voice', methods=['POST'])
def voice():
    resp = VoiceResponse()
    resp.say("Hello, please leave a message after the beep.")
    resp.record(timeout=5, transcribe=True, transcribe_callback='/transcribe')
    return str(resp)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    recording_url = request.form.get('RecordingUrl')
    if recording_url:
        transcribe_audio(recording_url)
    return "OK"


def transcribe_audio(recording_url):
    transcribe = boto3.client('transcribe')
    job_name = 'twilio_transcription_job'
    job_uri = recording_url
    language_code = 'en-US'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode=language_code,
        OutputBucketName='your-bucket-name'
    )
