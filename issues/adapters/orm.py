from sqlalchemy import (
    Table, Column, MetaData, String, Integer, Text, create_engine
)
from sqlalchemy.orm import mapper, scoped_session, sessionmaker, composite
from sqlalchemy_utils.functions import create_database, drop_database

from issues.domain.models import Issue, IssueReporter
from issues.domain.ports import UnitOfWork, UnitOfWorkManager


class SqlAlchemyUnitOfWorkManager(UnitOfWorkManager):

    def __init__(self, session_maker):
        self.session_maker = session_maker

    def start(self):
        return SqlAlchemyUnitOfWork(self.session_maker)


class IssueRepository:

    def __init__(self, session):
        self._session = session

    def add(self, issue):
        self._session.add(issue)


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, sessionfactory):
        self.sessionfactory = sessionfactory

    def __enter__(self):
        self.session = self.sessionfactory()
        return self

    def __exit__(self, type, value, traceback):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def issues(self):
        return IssueRepository(self.session)


class SqlAlchemy:

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self._session_maker = scoped_session(sessionmaker(self.engine),)

    @property
    def unit_of_work_manager(self):
        return SqlAlchemyUnitOfWorkManager(self._session_maker)

    def recreate_schema(self):
        drop_database(self.engine.url)
        create_database(self.engine.url)
        self.metadata.create_all()

    def get_session(self):
        return self._session_maker()

    def configure_mappings(self):
        self.metadata = MetaData(self.engine)

        IssueReporter.__composite_values__ = lambda i: (i.name, i.email)
        issues = Table(
            'issues',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('reporter_name', String(50)),
            Column('reporter_email', String(50)),
            Column('description', Text)
        )
        reporter_composition = composite(
            IssueReporter,
            issues.c.reporter_name,
            issues.c.reporter_email
        )
        properties = {
            'id': issues.c.id,
            'description': issues.c.description,
            'reporter': reporter_composition
        }
        mapper(Issue, issues, properties=properties)
