import datetime
import os
from typing import Annotated

from fastapi import Depends, FastAPI, Query, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select

class Entry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    iso_time: str
    lat: float | None = None
    lon: float | None = None

SQLITE_URL = "sqlite:///database.db"

engine = create_engine(SQLITE_URL, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/health", status_code=200)
def health():
    return "OK"

@app.get("/entries")
def get_entries(session: Annotated[Session, Depends(get_session)]) -> list[Entry]:
    return [entry for entry in session.exec(select(Entry)).all()]

@app.get("/entries/{id}")
def get_entry(id: int, session: Annotated[Session, Depends(get_session)]) -> Entry:
    result = session.get(Entry, id)
    if not result:
        raise HTTPException(status_code=404, detail="entry not found")
    return result

class EntryCreate(BaseModel):
    title: Annotated[str, Query(max_length=120)]
    body: str
    lat: float | None = None
    lon: float | None = None

@app.post("/entries", status_code=201)
def post_entry(body: EntryCreate, session: Annotated[Session, Depends(get_session)]) -> Entry:
    entry = Entry(
        title=body.title,
        body=body.body,
        iso_time=datetime.datetime.now().replace(microsecond=0).isoformat(),
        lat=body.lat,
        lon=body.lon,
    )

    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry
