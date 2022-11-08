# pylint: disable=missing-module-docstring
import sys
import os
import unittest
from datetime import datetime
from jira import Issue

# fix paths so tests can be run from project root
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)
# pylint: disable=wrong-import-position
from src.actions.issue_history import IssueHistory # pylint: disable=import-error


class TestIssueHistory(unittest.TestCase):

    def test_transition_formatting(self):
        """ Test that transitions are formatted as intended """
        timestamp = datetime(2022, 1, 1, 00, 00, 00)
        raw_dict = {
            "toString" : "Done",
            "field" : "Status"
        }
        testTransition = type(str('PropertyHolder'), (object,), raw_dict)
        # formatter String
        # f"\t {timestamp.strftime('%d/%m/%Y %H:%M')} {title} {transition.toString}"
        self.assertEqual("\t 01/01/2022 00:00 Status Done",
            IssueHistory.format_transition(testTransition, timestamp)
        )


    def test_unflagged(self):
        """ Test that unflagged transitions, those of type Flagged without a toString property, are handled """
        timestamp = datetime(2022, 1, 1, 00, 00, 00)
        raw_dict = {
            "toString" : "",
            "field" : "Flagged"
        }
        # Flagged type of transition with no "toString" property is an Unflag event
        testTransition = type(str('PropertyHolder'), (object,), raw_dict)
        self.assertIn("Unflagged",
            IssueHistory.format_transition(testTransition, timestamp)
        )

    def test_format_issue(self):
        """ Test that Issues are formatted as intended """
        raw_dict = {
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

        test_issue = Issue(options=None, session=None, raw=raw_dict)
        formatted_issue = IssueHistory.format_issue(test_issue)
        self.assertIn("\n[Epic: EPIC-1]\n", formatted_issue)
        self.assertIn("\nIssue : PROJECT-1 Issue Summary\n", formatted_issue)
        self.assertIn("\n\t 01/01/2022 00:00 Created\n", formatted_issue)
        self.assertIn( "\n\t 02/01/2022 00:00 Status In Progress", formatted_issue)
        self.assertIn( "\n\t 03/01/2022 00:00 Status Done", formatted_issue)

if __name__ == "__main__":
    unittest.main()
