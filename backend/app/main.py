from fastapi import FastAPI, Depends
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI Test"}