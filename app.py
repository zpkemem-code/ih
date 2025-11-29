# app.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Userbot API running"}
