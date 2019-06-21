import pytest

from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy.orm import clear_mappers

from issues.domain.models import Issue
from issues.domain.commands import ReportIssueCommand
from issues.services.handlers import ReportIssueHandler
from issues.adapters.orm import SqlAlchemy


NAME = 'Vovó Juju'
EMAIL = 'juju@abacate'
MESSAGE = 'Esqueci minha senha, bem'


class DB:

    def __init__(self):
        self.db = SqlAlchemy('sqlite://')

    def begin(self):
        self.db.configure_mappings()
        create_database(self.db.engine.url)
        self.db.metadata.create_all()

    def rollback(self):
        drop_database(self.db.engine.url)
        clear_mappers()


@pytest.fixture()
def data_base():
    return DB()


def report_an_issue(data_base):
    cmd = ReportIssueCommand(NAME, EMAIL, MESSAGE)
    handler = ReportIssueHandler(data_base.db.unit_of_work_manager)
    handler(cmd)


class TestWhenWeLoadAPersistedIssue:

    @pytest.fixture(autouse=True)
    def given_a_database_containing_an_issue(self, data_base):
        data_base.begin()
        report_an_issue(data_base)
        self.issues = data_base.db.get_session().query(Issue).all()
        yield
        data_base.rollback()

    def test_we_should_have_loaded_a_single_issue(self):
        assert len(self.issues) == 1

    def test_it_should_have_the_correct_description(self):
        assert self.issues[0].description == MESSAGE

    def test_it_should_have_the_correct_reporter_details(self):
        assert self.issues[0].reporter.name == NAME
        assert self.issues[0].reporter.email == EMAIL
