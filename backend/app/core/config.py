from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
#engine = create_engine(DATABASE_URL)
# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Base class for models
Base = declarative_base()

# Session local to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection to supabase successful!")
except Exception as e:
    print(f"Failed to connect: {e}")