from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2

app = FastAPI()

# Database Connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Define Database Model
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

# CORS Configuration (allows React frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI and BACKEND!"}

@app.get("/dbtest")
def db_test():
    """Check if database connection is working"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return {"db_version": db_version}
    except Exception as e:
        return {"error": str(e)}

# Pydantic Model for API Requests
class MessageCreate(BaseModel):
    text: str

# Endpoint to Add Message to Database
@app.post("/add_message/")
def add_message(msg: MessageCreate):
    db = SessionLocal()
    new_msg = Message(text=msg.text)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    db.close()
    return {"message": "Message added successfully!", "data": new_msg}

# Endpoint to Retrieve Messages from Database
@app.get("/messages/")
def get_messages():
    db = SessionLocal()
    messages = db.query(Message).all()
    db.close()
    return messages
