from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.templating import Jinja2Templates
from mangum import Mangum
import asyncio, json, uuid, boto3
from botocore.exceptions import ClientError
 
app = FastAPI()
 
 
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


'''
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/sync-site")
async def search(request: Request, query: str = Form(...)):
    # perform search logic
    results = ["Result 1", "Result 2", "Result 3"]
    return templates.TemplateResponse("search.html", {"request": request, "query": query, "results": results})
'''

@app.websocket("/audio")
async def audio(websocket: WebSocket):
    try:
        # Create an Amazon Transcribe streaming client
        client = boto3.client('transcribe', region_name='us-east-1')
        language_code = "en-US"

        # Generate a unique identifier for this transcription job
        job_name = str(uuid.uuid4())

        # Start the transcription job
        response = client.start_stream_transcription(
            LanguageCode=language_code,
            MediaSampleRateHertz=16000,
            MediaEncoding='pcm',
            AudioStream=websocket
        )

        # Initialize variables for speaker detection algorithm
        transcript = ""
        last_event_time = 0
        pause_threshold = 1.5  # Pause duration threshold in seconds

        # Keep streaming the audio data to Transcribe and handle the results
        async for message in websocket.iter_text():
            response = json.loads(message)
            results = response.get("Transcript", {}).get("Results", [])

            for result in results:
                if result.get("Alternatives"):
                    new_transcript = result["Alternatives"][0]["Transcript"]
                    confidence = result["Alternatives"][0]["Confidence"]
                    transcript += new_transcript

                    # Check if the speaker has stopped speaking
                    time_diff = result["ResultEndTime"] - last_event_time
                    if time_diff > pause_threshold:
                        # Send the transcript to the client
                        await websocket.send_text(f"Transcription: {transcript} (Confidence: {confidence})")

                        # Send the transcript to https://modal.com/ using an API request
                        response = requests.post("https://modal.com/api/transcripts", json={"transcript": transcript})
                        if response.status_code == 200:
                            await websocket.send_text(f"Transcript sent to https://modal.com/")
                        else:
                            await websocket.send_text(f"Failed to send transcript to https://modal.com/")

                        # Reset variables for the next speaker
                        transcript = ""
                    last_event_time = result["ResultEndTime"]

    except ClientError as e:
        await websocket.send_text(f"Error: {e}")
    except Exception as e:
        await websocket.send_text(f"Error: {e}")
 


handler = Mangum(app)