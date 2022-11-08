# pylint: disable=missing-module-docstring
import sys
import os
import unittest
from jira import Issue

# fix paths so tests can be run from project root
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)
# pylint: disable=wrong-import-position
from src.actions.csv import CSV # pylint: disable=import-error


class TestCsv(unittest.TestCase):
    def test_csv(self):
        """ Test that an Issue is formatted as CSV correctly to comply with the Header fields """
        # "issueKey, Epic Link, summary, created, started, completed"

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
        formatted_issue = CSV.format_issue(test_issue)
        test_line = "PROJECT-1,"                # issueKey
        test_line += "EPIC-1,"                  # Epic Link
        test_line += "\"Issue Summary\","       # Issue Summary
        test_line += "\"01/01/2022 00:00\","    # Created
        test_line += "\"02/01/2022 00:00\","    # started (moved to 'In Progress')
        test_line += "\"03/01/2022 00:00\""     # completed (moved to 'Done')
        self.assertEqual(test_line, formatted_issue)


    def test_csv_no_in_progress(self):
        """ Test that an issue without a transition to 'In Progress' is handled"""
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
                    "created" : "2022-01-03T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Done",
                      "field" : "status" }]
                }] # histories
            } # changelog
        } # fromDict

        test_issue = Issue(options=None, session=None, raw=raw_dict)
        formatted_issue = CSV.format_issue(test_issue)
        test_line = "PROJECT-1,"                # issueKey
        test_line += "EPIC-1,"                  # Epic Link
        test_line += "\"Issue Summary\","       # Issue Summary
        test_line += "\"01/01/2022 00:00\","    # Created
        test_line += ","                        # started (no 'In Progress')
        test_line += "\"03/01/2022 00:00\""     # completed (moved to 'Done')
        self.assertEqual(test_line, formatted_issue)

if __name__ == "__main__":
    unittest.main()
