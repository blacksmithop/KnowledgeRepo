from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import knowledge_repo

VERSION = "0.1.0"
DESCRIPTION = "A FastAPI server to for my knowledge repository"


app = FastAPI(version=VERSION, description=DESCRIPTION)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


routers = [knowledge_repo]

for item in routers:
    app.include_router(item.router)


@app.get("/version")
async def version():
    return {"version": VERSION}
