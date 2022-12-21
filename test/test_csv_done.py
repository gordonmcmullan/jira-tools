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
from src.actions.csv_done import CsvDone # pylint: disable=import-error


class TestCsvDone(unittest.TestCase):
    def test_csv_done(self):
        """ Test that an Issue is formatted as CSV correctly to comply with the Header fields """

        raw_dict = {
            "key" : "PROJECT-1",
            "id" : "00001",
            "fields" : {
                "created" : "2022-01-01T00:00:00.000+00:00",
                "updated" : "2022-01-04T00:00:00.000+00:00",
                "summary" : "Issue Summary",
                "customfield_10008" : "EPIC-1",
                "resolution" : {
                    "name" : "Done"
                },
                "status" : {
                    "name" : "Closed"
                },
                "priority" : {
                    "name" : "standard"
                },
                "issuetype" : {
                    "name" : "Issue"
                },
                "assignee" : {
                    "name" : "assignee.name"
                },
                "reporter" : {
                    "name" : "reporter.name"
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
        formatted_issue = CsvDone.format_issue(test_issue)
        test_line = "Issue,"                    # issue type
        test_line += "PROJECT-1,"                # issue Key
        test_line += "00001,"                    # issue id
        test_line += "\"Issue Summary\","       # Issue Summary
        test_line += "\"assignee.name\","       # Asignee
        test_line += "\"reporter.name\","       # reporter
        test_line += "\"standard\","            # priority
        test_line += "\"Closed\","              # status
        test_line += "\"Done\","                # resolution
        test_line += "\"01/01/2022 00:00\","    # Created
        test_line += "\"04/01/2022 00:00\","    # updated
        test_line += "EPIC-1,"                  # Epic Link
        test_line += "\"=NETWORKDAYS(Nx,Ox)\"," # Formula placeholder
        test_line += "\"02/01/2022 00:00\","    # started (moved to 'In Progress')
        test_line += "\"03/01/2022 00:00\""     # completed (moved to 'Done')
        self.assertEqual(test_line, formatted_issue)
