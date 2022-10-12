import unittest
import sys
import os

from jira import Issue


PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)

from datetime import datetime, timezone
from src.cli import Actions
from src.actions.issue_history import IssueHistory

class TestIssueHistory(unittest.TestCase):

    def test_transition_formatting(self):
        timestamp = datetime(2022, 1, 1, 00, 00, 00)
        fromDict = {
            "toString" : "Done",
            "field" : "Status"
        }    
        testTransition = type(str('PropertyHolder'), (object,), fromDict)
        # formatter String
        # f"\t {timestamp.strftime('%d/%m/%Y %H:%M')} {title} {transition.toString}"
        self.assertEquals("\t 01/01/2022 00:00 Status Done", 
            IssueHistory.format_transition(testTransition, timestamp)
        )


    def test_unflagged(self):
        timestamp = datetime(2022, 1, 1, 00, 00, 00)
        fromDict = {
            "toString" : "",
            "field" : "Flagged"
        }
        # Flagged type of transition with no "toString" property is an Unflag event
        testTransition = type(str('PropertyHolder'), (object,), fromDict)
        self.assertIn("Unflagged", 
            IssueHistory.format_transition(testTransition, timestamp)
        )

    def test_format_issue(self):
        
        fromDict = { 
            "key" : "PROJECT-1",
            "id" : "00001",
            "fields" : {
                "created" : "2022-01-01T00:00:00.000+00:00",
                "summary" : "Issue Summary",
                "customfield_10008" : "EPIC-1",
                "issuetype" : {
                    "name" : "Issue"
                }}, # fields
            "changelog" : {
                "histories" : [{ 
                    "created" : "2022-01-02T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "In Progress",
                      "field" : "status" }]
                },{ 
                    "created" : "2022-01-03T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Done",
                      "field" : "status" }]
                }] # histories
            } # changelog
        } # fromDict

        test_issue = Issue(options=None, session=None, raw=fromDict)
        formatted_issue = IssueHistory.format_issue(test_issue)
        self.assertIn("\n[Epic: EPIC-1]\n", formatted_issue)
        self.assertIn("\nIssue : PROJECT-1 Issue Summary\n", formatted_issue)
        self.assertIn("\n\t 01/01/2022 00:00 Created\n", formatted_issue)
        self.assertIn( "\n\t 02/01/2022 00:00 Status In Progress", formatted_issue)
        self.assertIn( "\n\t 03/01/2022 00:00 Status Done", formatted_issue)

if __name__ == "__main__":
    unittest.main()