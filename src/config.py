#pylint: disable=too-few-public-methods,missing-function-docstring,missing-module-docstring

from jira import JIRA

class Config:
    """ Config - contains useful configuration settings """
    def __init__(self,
                 project: str,
                 jira_url: str,
                 weeks: int) -> None:
        self.args = []

        self.project = project

        if jira_url != "":
            self.jira = JIRA(jira_url)
        else:
            self.jira = JIRA("http://localhost:2990/")

        if weeks:
            assert 0 <= weeks <= 52
            self.weeks = weeks
        else:
            self.weeks = 4
