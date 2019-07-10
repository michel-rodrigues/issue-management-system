import json
import pytest
import uuid
from unittest import mock

from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy.orm import clear_mappers

from .utils import SetupTestDBManager

from issues.adapters.flask import app
from issues.adapters.orm import SqlAlchemy
from issues.domain.commands import ReportIssueCommand
from issues.domain.models import Issue
from issues.services.handlers import ReportIssueHandler


ID = uuid.uuid4()
NAME = 'Vovó Juju'
EMAIL = 'juju@abacate'
MESSAGE = 'Come abacate, bem'

ID2 = uuid.uuid4()
NAME2 = 'Vovó Gigi'
EMAIL2 = 'gigi@chinelo'
MESSAGE2 = 'Sai da frente da TV'


@pytest.fixture()
def setup_data_base():
    return SetupTestDBManager()


class TestWhenReportingANewIssue:

    def make_http_post_request(self):
        data = json.dumps({
            'reporter_name': NAME,
            'reporter_email': EMAIL,
            'problem_description': MESSAGE,
        })
        url = '/issues/'
        content_type = 'application/json'
        http_post = app.test_client().post
        with mock.patch('issues.adapters.flask.db', self.setup_data_base.db):
            self.response = http_post(url, data=data, content_type=content_type)

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self, setup_data_base):
        self.setup_data_base = setup_data_base
        self.setup_data_base.begin()
        self.make_http_post_request()
        self.issues = self.setup_data_base.db.get_session().query(Issue).all()
        yield
        self.setup_data_base.rollback()

    def test_it_should_return_the_correct_status_code(self):
        assert self.response.status == '201 CREATED'
        assert self.response.status_code == 201

    def test_it_should_have_created_a_new_issue(self):
        assert len(self.issues) == 1

    def test_it_should_have_the_correct_description(self):
        assert self.issues[0].description == MESSAGE

    def test_it_should_have_the_correct_reporter_details(self):
        assert self.issues[0].reporter.name == NAME
        assert self.issues[0].reporter.email == EMAIL


class TestWhenRetrievingASpecificIssue:

    def report_an_issue(self):
        db = self.setup_data_base.db
        cmd = ReportIssueCommand(ID, NAME, EMAIL, MESSAGE)
        handler = ReportIssueHandler(db.unit_of_work_manager)
        handler(cmd)

    def make_http_get_request(self):
        url = f'/issues/{self.issue.id}/'
        client = app.test_client()
        with mock.patch('issues.adapters.flask.db', self.setup_data_base.db):
            self.response = client.get(url)

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self, setup_data_base):
        self.setup_data_base = setup_data_base
        self.setup_data_base.begin()
        self.report_an_issue()
        self.issue = self.setup_data_base.db.get_session().query(Issue).all()[0]
        self.make_http_get_request()
        yield
        self.setup_data_base.rollback()

    def test_it_should_return_the_correct_status_code(self):
        assert self.response.status == '200 OK'
        assert self.response.status_code == 200

    def test_it_should_retrieve_the_correct_reporter_details(self):
        assert self.response.json['reporter_name'] == NAME
        assert self.response.json['reporter_email'] == EMAIL

    def test_it_should_retrieve_the_correct_description(self):
        assert self.response.json['description'] == MESSAGE


class TestWhenListingIssues:

    def report_an_issue(self, id, name, email, message):
        db = self.setup_data_base.db
        cmd = ReportIssueCommand(id, name, email, message)
        handler = ReportIssueHandler(db.unit_of_work_manager)
        handler(cmd)

    def make_http_get_request(self):
        url = '/issues/'
        client = app.test_client()
        with mock.patch('issues.adapters.flask.db', self.setup_data_base.db):
            self.response = client.get(url)

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self, setup_data_base):
        self.setup_data_base = setup_data_base
        self.setup_data_base.begin()
        self.report_an_issue(ID, NAME, EMAIL, MESSAGE)
        self.report_an_issue(ID2, NAME2, EMAIL2, MESSAGE2)
        self.make_http_get_request()
        yield
        self.setup_data_base.rollback()

    def test_it_should_have_retrieved_all_issues(self):
        assert len(self.response.json) == 2

    def test_it_should_retrived_the_list_with_correct_vovo_juju_data(self):
        assert self.response.json[0]['issue_id'] == str(ID)
        assert self.response.json[0]['reporter_name'] == NAME
        assert self.response.json[0]['reporter_email'] == EMAIL
        assert self.response.json[0]['description'] == MESSAGE

    def test_it_should_retrived_the_list_with_correct_vovo_gigi_data(self):
        assert self.response.json[1]['issue_id'] == str(ID2)
        assert self.response.json[1]['reporter_name'] == NAME2
        assert self.response.json[1]['reporter_email'] == EMAIL2
        assert self.response.json[1]['description'] == MESSAGE2
