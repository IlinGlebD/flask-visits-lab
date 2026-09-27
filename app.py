import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, request
from sqlalchemy import create_engine, DateTime, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session
)


load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    visited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False
    )


Base.metadata.create_all(engine)


app = Flask(__name__)


@app.get("/hello")
def hello():
    current_time = datetime.now(timezone.utc)

    client_ip = request.remote_addr or "unknown"

    visit = Visit(
        visited_at=current_time,
        ip_address=client_ip
    )

    with Session(engine) as session:
        session.add(visit)
        session.commit()

    return "Hello", 200
