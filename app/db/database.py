from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import get_config
import os

settings = get_config(config=os.getenv("env") or 'dev')

# url = "mysql+pymysql://sai:sai@localhost:3306/test"

engine = create_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def connect_to_db():
    engine.connect()
    print("Database connected.")


def create_tables():
    Base.metadata.create_all(engine)