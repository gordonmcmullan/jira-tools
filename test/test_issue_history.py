import unittest
import sys
import os

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)

from datetime import datetime, timezone
from src.cli import Actions
from src.actions.issue_history import IssueHistory

class TestIssueHistory(unittest.TestCase):

    def test_formatting(self):
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
        testTransition = type(str('PropertyHolder'), (object,), fromDict)
        self.assertIn("Unflagged", 
            IssueHistory.format_transition(testTransition, timestamp)
        )

if __name__ == "__main__":
    unittest.main()