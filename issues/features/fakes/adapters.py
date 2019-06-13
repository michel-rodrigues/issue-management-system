from domain.models import IssueLog


class FakeIssueLog(IssueLog):

    def __init__(self):
        self.issues = []

    def add(self, issue):
        self.issues.append(issue)

    def __len__(self):
        return len(self.issues)

    def __getitem__(self, idx):
        return self.issues[idx]
