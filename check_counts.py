from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def cleanup_old_tables():
    db = SessionLocal()
    try:
        # Check counts in all tables to be safe
        for table in ['conversations', 'chat_history', 'conversations_v2', 'chat_history_v2']:
            try:
                res = engine.execute(f"SELECT COUNT(*) FROM {table}").scalar()
                print(f"Table {table}: {res} rows")
            except Exception as e:
                print(f"Table {table} check failed: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    cleanup_old_tables()
