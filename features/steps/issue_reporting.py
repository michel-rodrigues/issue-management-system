from behave import given, when, then

from issues.domain.commands import ReportIssueCommand
from issues.services.handlers import ReportIssueHandler

from features.fakes.adapters import FakeUnitOfWork


NAME = 'Vovó Juju'
EMAIL = 'juju@abacate'
DESCRIPTION = 'Esqueci minha senha, bem'


class WhenReportingAnIssue:

    @given('an empty issue log')
    def given_an_empty_issue_log(self):
        self.unit_of_work = FakeUnitOfWork()

    @when('we report a new issue')
    def because_we_report_a_new_issue(self):
        handler = ReportIssueHandler(self.unit_of_work)
        cmd = ReportIssueCommand(NAME, EMAIL, DESCRIPTION)
        handler(cmd)

    @then('it should have created a new issue')
    def the_handler_should_have_created_a_new_issue(self):
        assert len(self.unit_of_work.issues) == 1

    @then('it should have recorded the issuer')
    def it_should_have_recorded_the_issuer(self):
        assert self.unit_of_work.issues[0].reporter.name == NAME
        assert self.unit_of_work.issues[0].reporter.email == EMAIL

    @then('it should have recorded the description')
    def it_should_have_recorded_the_description(self):
        assert self.unit_of_work.issues[0].description == DESCRIPTION

    @then('it should have committed the unit of work')
    def it_should_have_committed_the_unit_of_work(self):
        assert self.unit_of_work.was_committed is True
