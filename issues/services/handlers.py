from issues.domain.models import Issue, IssueReporter


class ReportIssueHandler:

    def __init__(self, unit_of_work):
        self.unit_of_work = unit_of_work

    def __call__(self, cmd):
        reported_by = IssueReporter(cmd.reporter_name, cmd.reporter_email)
        issue = Issue(cmd.issue_id, reported_by, cmd.problem_description)
        with self.unit_of_work.start() as tx:
            tx.issues.add(issue)
            tx.commit()
