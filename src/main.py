import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api_v1 import api
from core.config import settings


if not os.path.isdir('statics'):
    os.mkdir('statics')

if not os.path.isdir('media'):
    os.mkdir('media')

app = FastAPI(title='Introduction')
app.mount("/statics", StaticFiles(directory="statics"), name="statics")
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/", tags=['Default'])
async def root():
    return {"message": "Hello Bigger Applications!"}


app.include_router(api.api_v1_router, prefix=settings.API_V1_NAME)


if __name__ == '__main__':
    uvicorn.run(app, port=settings.SERVER_PORT)
    