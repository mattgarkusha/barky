from typing import Text
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    event,
    create_engine,
    inspect
)

from sqlalchemy.orm import registry

from domain.model import Bookmark
from config import Config

mapper_registry = registry()


if Config.TESTING:
    engine = create_engine("sqlite:///:memory:", echo=True)
else:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

bookmarks = Table(
    "bookmarks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), unique=True),
    Column("url", String(255)),
    Column("notes", Text),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)


def start_mappers():
    print("**** starting mappers ****")
    bookmarks_mapper = mapper_registry.map_imperatively(Bookmark, bookmarks)

def create_tables():
    with engine.connect() as conn:
        if not inspect(engine).has_table("bookmarks"):
            print('**** creating tables ****')
            mapper_registry.metadata.create_all(engine)
            print('**** tables created ****')

def drop_tables():
    print('**** dropping tables ****')
    mapper_registry.metadata.drop_all(engine)
    print('**** tables dropped ****')

@event.listens_for(Bookmark, "load")
def receive_load(bookmark, _):
    bookmark.events = []