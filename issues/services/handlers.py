from domain.models import Issue, IssueReporter


class ReportIssueHandler:

    def __init__(self, issue_log):
        self.issue_log = issue_log

    def __call__(self, cmd):
        reported_by = IssueReporter(cmd.reporter_name, cmd.reporter_email)
        issue = Issue(reported_by, cmd.problem_description)
        self.issue_log.add(issue)
