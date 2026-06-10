from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gold_monitorings.db")

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,# this will not update anything until there is db.commit()
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    return SessionLocal()
   
