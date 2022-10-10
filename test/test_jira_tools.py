import jira_tools
import sys

import unittest

from datetime import datetime, timezone

from jira_tools.formatters import IssueHistory


class NumberToText(unittest.TestCase):

    def test_number_to_text(self):
        text = ["zero", "one", "two", "three", "four", "five", "six",
                "seven", "eight", "nine", "ten", "eleven", "twelve"]
        for number in range(1, 12):
            self.assertEqual(jira_tools.number_to_text(number), text[number])

class FormatIssue(unittest.TestCase):

    class TestIssuetype():
        name = "Task"

    class IssueFields():
        issuetype = None
        customfield_10008 = "CIPI-1"
        created = "2022-01-01T00:00:00.000+0000"
    
    class TestIssue():
        key = "CIPI-2"
        fields = None
        


    """         "\n",
                issue.fields.issuetype.name, ":", issue.key,
                "Epic: ", issue.fields.customfield_10008,
                "\n\t",
                iso8601.parse_date(
                    issue.fields.created).strftime('%d/%m/%Y %H:%M'),
                "Created"
    """

    def test_format_issue(self):
            print(sys.path)

            test_issue = self.TestIssue()
            test_issue.fields = self.IssueFields()
            test_issue.fields.issuetype = self.TestIssuetype()
            test_issue.fields.summary = "Test"
            formatted_issue = IssueHistory.format_issue(test_issue)
            print(formatted_issue)
            self.assertIn("CIPI-2", formatted_issue)
            self.assertIn("01/01/2022 00:00", formatted_issue)


class FormatTransition(unittest.TestCase):

    class TestTransition():
        field = "Status"
        fieldtype = "jira"
        fromString = "Backlog"
        toString = "Selected for Development"


    def test_format_transition(self):
        timestamp = datetime(2022, 1, 1, 00, 00, 00, tzinfo=timezone.utc)
        test_transition = self.TestTransition()
        formatted_transition = IssueHistory.format_transition(test_transition, timestamp)
        self.assertIn("Selected for Development", formatted_transition)
        self.assertIn("01/01/2022 00:00", formatted_transition)
        self.assertIn("Status", formatted_transition)


if __name__ == "__main__":
    unittest.main()