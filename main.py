#!/usr/bin/python

# imports
import uvicorn, os
from fastapi import FastAPI
from fastapi import Request
from starlette.templating import Jinja2Templates
from starlette.responses import Response
from mod.api import API
from mod.utils import print_log

# Create server
app = FastAPI()
templates = Jinja2Templates('templates')

# Server home page
@app.get('/')
def home_page(request: Request):
    print_log(f'"/" - {request.client.host}', 'INFO', 'WEB')
    return templates.TemplateResponse('index.html', {'request': request})

# Create server
@app.get('/create')
def api_page(request: Request):
    return API.create()

# Start server
if __name__ == "__main__":
    # dev
    uvicorn.run('main:app',
        host="0.0.0.0", 
        port=8000,
        log_level="debug",
        http="h11",
        reload=True, 
        use_colors=True,
        workers=3
    )
    # prod
    #uvicorn.run('app:app',
    #    host="0.0.0.0", 
    #    port=80,
    #    http="h11"
    #)