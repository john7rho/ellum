from fastapi import FastAPI, Request, Form, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum
import asyncio, json, uuid, boto3, aiohttp
from botocore.exceptions import ClientError
import requests



app = FastAPI()
 
templates = Jinja2Templates(directory="templates")

# Mount the 'static' and 'templates' directories to serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sync-site")
async def index(request: Request):

    return templates.TemplateResponse("process.html", {"request": request})

@app.post("/sync-site", response_class=HTMLResponse)
async def sync_site(request: Request, url_input: str = Form()):
    # Here you can do something with the submitted URL
    if url_input != "":
        cache_data = "https://adityarai10101--vectordbqaadi-queryurl.modal.run/?url="+str(url_input)
        sync_cache = requests.get(cache_data)
        print(sync_cache)
    else:
        raise HTTPException(status_code=404, detail="URL cannot be empty")

    return templates.TemplateResponse("process.html", {"request": request, "query": url_input, "status": "Successfully synced "+str(url_input)+"!"})

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
#https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse


async def transcribe_audio(language_code: str, websocket: WebSocket):
    try:
        # Create an Amazon Transcribe streaming client
        client = boto3.client('transcribe', region_name='us-east-1')

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
                if result.get("IsPartial") == False and result.get("Alternatives"):
                    new_transcript = result["Alternatives"][0]["Transcript"]
                    confidence = result["Alternatives"][0]["Confidence"]
                    transcript += new_transcript

                    # Check if the speaker has stopped speaking
                    time_diff = result["ResultEndTime"] - last_event_time
                    if time_diff > pause_threshold:
                        # Send the transcript to the external API
                        async with aiohttp.ClientSession() as session:
                            url = "https://adityarai10101--vectordbqaadi-queryreal.modal.run/?x=how+many+products+do+you+sell"
                            payload = {"transcription": transcript, "confidence": confidence}
                            async with session.post(url, json=payload) as response:
                                pass

                        # Yield the transcript to the client
                        yield f"Transcription: {transcript} (Confidence: {confidence})\n"

                        # Reset variables for the next speaker
                        transcript = ""
                    last_event_time = result["ResultEndTime"]

            # Release the event loop to allow other coroutines to run
            await asyncio.sleep(0)

    except ClientError as e:
        logger.exception(f"Transcription job {job_name} failed: {e}")
    except Exception as e:
        logger.exception(f"Transcription job {job_name} failed: {e}")

@app.websocket("/audio")
async def audio(websocket: WebSocket):
    language_code = "en-US"

    # Return the transcription as a stream of responses
    return StreamingResponse(transcribe_audio(language_code, websocket))

handler = Mangum(app)