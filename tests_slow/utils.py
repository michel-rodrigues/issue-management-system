from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy.orm import clear_mappers

from issues.adapters.orm import SqlAlchemy


class SetupTestDBManager:

    def __init__(self):
        self.db = SqlAlchemy('sqlite://')

    def begin(self):
        clear_mappers()
        self.db.configure_mappings()
        create_database(self.db.engine.url)
        self.db.metadata.create_all()

    def rollback(self):
        drop_database(self.db.engine.url)
        clear_mappers()
