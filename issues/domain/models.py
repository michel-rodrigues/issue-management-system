import abc


class IssueReporter:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Issue:
    def __init__(self, reporter, description):
        self.description = description
        self.reporter = reporter


class IssueLog(abc.ABC):

    @abc.abstractmethod
    def add(self, issue):
        pass
