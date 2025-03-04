from fastapi import FastAPI, Depends
from pydantic import BaseModel
from backend.app.api.routers.profile import router as profile_router


app = FastAPI()

# Include the profile_router in the app.
app.include_router(profile_router)

@app.get("/")
def home():
    return {"message": "FastAPI Test Route"}