import os

from sqlalchemy_utils.functions import create_database
from issues.adapters.orm import SqlAlchemy


if __name__ == "__main__":
    if os.path.exists('issues.db'):
        os.remove('issues.db')
    db = SqlAlchemy('sqlite:///issues.db')
    create_database(db.engine.url)
    db.configure_mappings()
    db.metadata.create_all()
