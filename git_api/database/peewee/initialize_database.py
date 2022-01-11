from pathlib import Path

from .models import (
    database as peewee_database,
    BaseModel,
)
from database.provide_database import IDatabaseInitializer


class DatabaseInitializerPeewee:
    def __init__(self):
        assert isinstance(self, IDatabaseInitializer)

    @staticmethod
    def init_db(db_path: Path) -> None:
        peewee_database.init(db_path, pragmas={"foreign_keys": 1})

    @staticmethod
    def create_empty_database(db_path: Path) -> None:
        models = BaseModel.__subclasses__()
        peewee_database.init(db_path, pragmas={"foreign_keys": 1})
        peewee_database.connect()
        peewee_database.create_tables(models)

    @staticmethod
    def reconnect(db_path: Path) -> None:
        peewee_database.close()
        peewee_database.init(db_path, pragmas={"foreign_keys": 1})
        peewee_database.connect()
