import unittest
import jira_tools


class NumberToText(unittest.TestCase):

    def test_number_to_text(self):
        text = ["zero", "one", "two", "three", "four", "five", "six",
                "seven", "eight", "nine", "ten", "eleven", "twelve"]
        for number in range(1, 12):
            self.assertEqual(jira_tools.number_to_text(number), text[number])
