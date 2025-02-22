from fastapi import FastAPI
from core.config import engine, Base
from models.profile import Profile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create DB and tables
def create_db_and_tables():
    try:
        logger.info("Attempting to create database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating the database tables {e}")
        raise

# Create DB and tables
create_db_and_tables()

# Initialize FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Test"}