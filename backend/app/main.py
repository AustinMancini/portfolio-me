from fastapi import FastAPI

# Initialize FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Test"}