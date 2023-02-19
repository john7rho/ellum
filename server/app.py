from fastapi import FastAPI, Request, Form, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum
import asyncio, json, uuid, boto3, aiohttp
from botocore.exceptions import ClientError, BotoCoreError
import requests

app = FastAPI()
 
templates = Jinja2Templates(directory="templates")

# Mount the 'static' and 'templates' directories to serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", name="home")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sync-site", name="sync")
async def index(request: Request):

    return templates.TemplateResponse("process.html", {"request": request})

@app.post("/sync-site", response_class=HTMLResponse, name="sync")
async def sync_site(request: Request, url_input: str = Form()):
    # Here you can do something with the submitted URL
    if url_input != "":
        cache_data = "https://adityarai10101--vectordbqaadi-queryurl.modal.run/?url="+str(url_input)
        sync_cache = requests.get(cache_data)
        print(sync_cache)
    else:
        raise HTTPException(status_code=404, detail="URL cannot be empty")

    return templates.TemplateResponse("process.html", {"request": request, "query": url_input, "status": "Successfully synced "+str(url_input)+"!"})

handler = Mangum(app)