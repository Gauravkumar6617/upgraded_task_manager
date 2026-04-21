from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import get_settings
from sqlalchemy.ext.declarative import declarative_base
settings = get_settings()

# 1. Create the engine ONCE. 
# connect_args is crucial for SQLite + FastAPI!
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

# 2. Create the Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
# 3. The "Dependency" - This is the professional way to handle sessions
def get_db():
    db = SessionLocal()
    try:
        yield db  # This sends the session to your API route
    finally:
        db.close() # This runs AFTER the API response is sent. VERY IMPORTANT!