from database import Base
from sqlalchemy import Column, PrimaryKeyConstraint, String, Integer

class hash_title(Base):
    __tablename__ = "gold_monitor"
    id = Column(Integer,primary_key=True, autoincrement=True)
    title = Column(String)