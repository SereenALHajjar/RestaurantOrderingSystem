from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
import app.models

postgres_url = "postgresql://postgres:postgres@localhost:5435/restaurant_db"

engine = create_engine(postgres_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
# Depends(get_session) is the metadata. It tells FastAPI how to get that Session.

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Key Differences:
# Engine:
# Manages database connections.
# Created once per application (typically).
# Represents the database itself.
# Session:
# Manages a unit of work (a series of database operations).
# Created and closed for each request (or a specific transaction).
# Represents a temporary workspace for interacting with data.


