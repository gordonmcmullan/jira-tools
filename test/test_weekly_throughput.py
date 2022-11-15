# pylint: disable=missing-module-docstring
import unittest
import sys
import os

# fix paths so tests can be run from project root
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)

from src.actions.weekly_throughput import WeeklyThroughput as WT # pylint: disable=import-error,wrong-import-position

class NumberToText(unittest.TestCase):

    def test_number_to_text(self):
        text = ["zero", "one", "two", "three", "four", "five", "six",
                "seven", "eight", "nine", "ten", "eleven", "twelve"]
        for number in range(1, 12):
            self.assertEqual(WT.number_to_text(number), text[number])


if __name__ == "__main__":
    unittest.main()
