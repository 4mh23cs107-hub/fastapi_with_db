from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import Conversation, ChatHistory

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def check_db():
    db = SessionLocal()
    try:
        convs = db.query(Conversation).all()
        print(f"Total Conversations: {len(convs)}")
        for c in convs:
            print(f"ID: {c.id}, Title: {c.title}")
        
        hist = db.query(ChatHistory).all()
        print(f"Total Messages: {len(hist)}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
