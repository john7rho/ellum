import boto3
import requests
from flask import Flask, request, Response

# Set up Flask app
app = Flask(__name__)


# Define endpoint URL for Twilio to send audio stream


@app.route("/transcribe", methods=['POST'])
def transcribe_audio():
    # Set up Amazon Transcribe client
    transcribe = boto3.client('transcribe', aws_access_key_id='AKIASYSAF2CEXXUGTFFP',
                              aws_secret_access_key='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', region_name='us-west-2')

    # Get the audio data from Twilio
    audio_data = request.get_data()
    # Set up parameters for the Amazon Transcribe job
    job_name = "transcription-job"
    media_sample_rate_hz = 8000
    media_format = "audio/wav"
    language_code = "en-US"
    # Start the Amazon Transcribe job
    response = transcribe.start_stream_transcription(
        LanguageCode=language_code,
        MediaFormat=media_format,
        MediaSampleRateHertz=media_sample_rate_hz,
        AudioStream={
            'AudioEvent': {
                'AudioChunk': audio_data
            }
        },
        # Set up the callback URL for when the transcription job is completed
        OutputBucketName='my-transcription-bucket',
        OutputKey='transcription-result',
        # Set up the callback URL for when the transcription job is completed
        # This URL should handle the transcription results from Amazon Transcribe
        # and take appropriate actions based on the results
        # CallbackUrl='https://my-callback-url.com/transcription-result'
    )
    return response
    # return Response(status=200)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port='5001')
