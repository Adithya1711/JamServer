# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For this example, we use SQLite. It's a simple file-based database.
# In production, you'd replace this with PostgreSQL, MySQL, etc.
SQLALCHEMY_DATABASE_URL = "sqlite:///./file_uploader.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of the SessionLocal class will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class that our ORM models will inherit from.
Base = declarative_base()

# Dependency to get a DB session in path operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

