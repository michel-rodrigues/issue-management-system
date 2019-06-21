import abc


class IssueReporter:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f'{self.name} <{self.email}>'


class Issue:
    def __init__(self, reporter, description):
        self.description = description
        self.reporter = reporter

    def __repr__(self):
        return f'<Issue: {self.reporter}>'


class IssueLog(abc.ABC):

    @abc.abstractmethod
    def add(self, issue):
        pass
