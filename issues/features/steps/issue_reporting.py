from behave import given, when, then

from domain.commands import ReportIssueCommand
from services.handlers import ReportIssueHandler

from features.fakes.adapters import FakeIssueLog


EMAIL = "bob@example.org"
NAME = "bob"
DESCRIPTION = "My mouse won't move"


class WhenReportingAnIssue:

    @given('an empty issue log')
    def given_an_empty_issue_log(self):
        self.issues = FakeIssueLog()

    @when('we report a new issue')
    def because_we_report_a_new_issue(self):
        handler = ReportIssueHandler(self.issues)
        cmd = ReportIssueCommand(NAME, EMAIL, DESCRIPTION)
        handler(cmd)

    @then('it should have created a new issue')
    def the_handler_should_have_created_a_new_issue(self):
        assert len(self.issues) == 1

    @then('it should have recorded the issuer')
    def it_should_have_recorded_the_issuer(self):
        assert self.issues[0].reporter.name == NAME
        assert self.issues[0].reporter.email == EMAIL

    @then('it should have recorded the description')
    def it_should_have_recorded_the_description(self):
        assert self.issues[0].description == DESCRIPTION
