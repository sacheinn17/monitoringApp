from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AppUsage(Base):
    __tablename__ = "AppUsage"

    id = Column(Integer,primary_key = True)
    appName = Column(String)
    context = Column(String)
    date = Column(String)
    usageTime = Column(Integer)
    catogary = Column(String)
    subCatogary = Column(String)

class rules(Base):
    __tablename__ = "rules"
    id = Column(Integer,primary_key = True)
    name = Column(String)
    context = Column(String)
    catogary = Column(String)
    subCatogary = Column(String)
    flip = Column(Boolean)
