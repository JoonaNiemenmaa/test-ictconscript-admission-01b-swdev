import datetime
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select
from starlette.exceptions import HTTPException

class Entry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    iso_time: str
    lat: float | None = None
    lon: float | None = None

DB_NAME = "database.db"
SQLITE_URL = f"sqlite:///{DB_NAME}"

engine = create_engine(SQLITE_URL, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/health", status_code=200)
def health():
    return "OK"

@app.get("/entries")
def get_entries() -> list[Entry]:
    with Session(engine) as session:
        return [entry for entry in session.exec(select(Entry)).all()]

@app.get("/entries/{id}")
def get_entry(id: int) -> Entry:
    with Session(engine) as session:
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
def post_entry(body: EntryCreate) -> Entry:
    entry = Entry(
        title=body.title,
        body=body.body,
        iso_time=datetime.datetime.now().replace(microsecond=0).isoformat(),
        lat=body.lat,
        lon=body.lon,
    )

    with Session(engine) as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry
