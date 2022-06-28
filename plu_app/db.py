from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import get_settings


engine = create_engine(
    get_settings().get_db_url(),
)

Session = sessionmaker(engine)


async def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
        