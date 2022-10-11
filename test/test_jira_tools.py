import unittest
import sys
import os

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)

from datetime import datetime, timezone
from src.jira_tools import number_to_text
from src.cli import Actions

from src.actions.issue_history import IssueHistory

class NumberToText(unittest.TestCase):

    def test_number_to_text(self):
        text = ["zero", "one", "two", "three", "four", "five", "six",
                "seven", "eight", "nine", "ten", "eleven", "twelve"]
        for number in range(1, 12):
            self.assertEqual(number_to_text(number), text[number])


if __name__ == "__main__":
    unittest.main()