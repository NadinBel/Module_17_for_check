from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import sqlite3
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///taskmanager.db', echo=True)

connection = engine.connect()
connection.execute('pragma foreign_keys=ON;')

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

