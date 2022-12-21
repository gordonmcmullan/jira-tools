# pylint: disable=missing-module-docstring
import os
import sys
import unittest

from jira import Issue


# pylint: disable=missing-module-docstring
# fix paths so tests can be run from project root
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)
# pylint: disable=wrong-import-position
from src.actions.csv_flagged import CsvFlagged # pylint: disable=import-error

class TestCsvFlaged(unittest.TestCase):
    def test_csv_flagged(self):
        """ Test that an Issue that has been flagged is formatted as CSV correctly to comply with the Header fields """
        #"issueKey,issuedId,Summary,\"Epic Link\",flagged,unflagged"

        #ToDo: create a TestIssue factory
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
                    { "toString" : "Impediment",
                      "field" : "flagged" }]
                },{
                    "created" : "2022-01-03T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "",
                      "field" : "flagged" }]
                }] # histories
            } # changelog
        } # fromDict

        test_issue = Issue(options=None, session=None, raw=raw_dict)
        formatted_issue = CsvFlagged.format_issue(test_issue)
        test_line = "PROJECT-1,"                # issueKey
        test_line += "00001,"                   # issueId
        test_line += "\"Issue Summary\","       # Issue Summary
        test_line += "EPIC-1,"                  # Epic Link
        test_line += "\"02/01/2022 00:00\","    # flagged
        test_line += "\"03/01/2022 00:00\"\n"   # unflagged
        self.assertEqual(test_line, formatted_issue)

    def test_closed_while_flagged(self):
        raw_dict = {
            "key" : "PROJECT-2",
            "id" : "00002",
            "fields" : {
                "created" : "2022-02-01T00:00:00.000+00:00",
                "summary" : "Issue Summary",
                "customfield_10008" : "EPIC-1",
                "issuetype" : {
                    "name" : "Issue"
                }}, # fields
            "changelog" : {
                "histories" : [{
                    "created" : "2022-02-02T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Impediment",
                      "field" : "flagged" }]
                },{
                    "created" : "2022-02-02T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Done",
                      "field" : "status" }]
                },{
                    "created" : "2022-02-03T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Closed",
                      "field" : "status" }]
                }] # histories
            } # changelog
        } # fromDict

        test_issue = Issue(options=None, session=None, raw=raw_dict)
        formatted_issue = CsvFlagged.format_issue(test_issue)
        test_line = "PROJECT-2,"                # issueKey
        test_line += "00002,"                   # issueId
        test_line += "\"Issue Summary\","       # Issue Summary
        test_line += "EPIC-1,"                  # Epic Link
        test_line += "\"02/02/2022 00:00\","    # flagged
        test_line += "\"03/02/2022 00:00\"\n"   # Closed = unflagged
        self.assertEqual(test_line, formatted_issue)

    def test_cloned_while_flagged(self):
        # this happens when an issue is cloned from another issue that is flagged at the time
        # (don't clone issues that aren't really clones)

        raw_dict = {
            "key" : "PROJECT-3",
            "id" : "00003",
            "fields" : {
                "created" : "2022-02-01T00:00:00.000+00:00",
                "summary" : "Issue Summary",
                "customfield_10008" : "EPIC-1",
                "issuetype" : {
                    "name" : "Issue"
                }}, # fields
            "changelog" : {
                "histories" : [{
                    "created" : "2022-03-02T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "",
                      "field" : "flagged" }]
                },{
                    "created" : "2022-03-02T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Done",
                      "field" : "status" }]
                },{
                    "created" : "2022-03-03T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Closed",
                      "field" : "status" }]
                }] # histories
            } # changelog
        } # fromDict

        test_issue = Issue(options=None, session=None, raw=raw_dict)
        formatted_issue = CsvFlagged.format_issue(test_issue)
        self.assertEqual("", formatted_issue)
