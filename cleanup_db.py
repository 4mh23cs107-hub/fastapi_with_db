from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import Conversation, ChatHistory

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def cleanup_db():
    db = SessionLocal()
    try:
        # Check counts before
        convs = db.query(Conversation).all()
        print(f"Total Conversations before cleanup: {len(convs)}")
        
        # 1. DELETE ALL CONVERSATIONS (This should be tied to the current user in production, but we'll do all for testing)
        # Note: We need to delete ChatHistory first if there are no cascades
        db.query(ChatHistory).delete()
        db.query(Conversation).delete()
        
        db.commit()
        print("Cleanup successful!")
        
        # Verify
        convs_after = db.query(Conversation).all()
        print(f"Total Conversations after cleanup: {len(convs_after)}")
        
    except Exception as e:
        db.rollback()
        print(f"Cleanup failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_db()
