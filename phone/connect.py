import boto3
import time

# create an Amazon Connect client
connect = boto3.client('connect')

# create a contact flow that starts transcription
contact_flow = {
    "StartAction": {
        "TranscriptionSettings": {
            "TranscriptionEnabled": True,
            "LanguageCode": "en-US",
            "MediaEncoding": "pcm",
            "VocabularyName": "my-vocabulary" #optional, if you have a custom vocabulary
        }
    },
    "States": {
        "Start": {
            "Type": "ConnectStartFlow",
            "Parameters": {
                "InstanceArn": "your-instance-arn",
                "ContactFlowId": "your-contact-flow-id",
                "Attributes": {
                    "AttributeName1": "AttributeValue1",
                    "AttributeName2": "AttributeValue2"
                }
            },
            "Next": "End"
        },
        "End": {
            "Type": "Disconnect"
        }
    }
}

# create a phone number to associate with the contact flow
response = connect.create_routing_profile(
    Name='my-routing-profile',
    DefaultOutboundQueueId='my-queue-id',
)
routing_profile_id = response['RoutingProfileId']
response = connect.create_routing_profile_queue_reference(
    RoutingProfileId=routing_profile_id,
    QueueId='my-queue-id'
)
response = connect.create_phone_number(
    PhoneNumber='+1234567890',
    PhoneNumberCountryCode='US',
    Name='my-phone-number',
    Description='My phone number for transcription demo',
    RoutingProfileId=routing_profile_id,
    PhoneNumberType='DID'
)
phone_number_id = response['PhoneNumberId']

# initiate a contact to the phone number and start transcription
response = connect.start_outbound_voice_contact(
    DestinationPhoneNumber='+1234567890',
    ContactFlowId='your-contact-flow-id',
    InstanceId='your-instance-id',
    Attributes={
        'AttributeName1': 'AttributeValue1',
        'AttributeName2': 'AttributeValue2'
    },
    QueueId='my-queue-id',
    SourcePhoneNumber='+9876543210'
)
contact_id = response['ContactId']
print(f"Contact initiated with contact ID {contact_id}.")

# wait for the contact to be connected and transcribing
while True:
    response = connect.get_contact(
        ContactId=contact_id
    )
    contact_status = response['ContactStatus']
    if contact_status in ['CONNECTED', 'IN_PROGRESS']:
        transcription_status = response['Transcript']['TranscriptStatus']
        if transcription_status == 'IN_PROGRESS':
            transcript = response['Transcript']['TranscriptFileUri']
            print(f"Transcription in progress: {transcript}")
            break
    time.sleep(5)

# continuously monitor the transcription
while True:
    response = connect.get_contact(
        ContactId=contact_id
    )
    transcript_status = response['Transcript']['TranscriptStatus']
    if transcript_status == 'COMPLETED':
        transcript = response['Transcript']['TranscriptFileUri']
        print(f"Transcription completed: {transcript}")
        break
    elif transcript_status == 'IN_PROGRESS':
        transcript = response['Transcript']['TranscriptFileUri']
        transcript_file = requests.get(transcript).text
        transcription = json.loads(transcript_file)
        results = transcription['results']['transcripts'][0]['transcript']
        print(f"Transcription in progress: {results}")
    time.sleep(5)
