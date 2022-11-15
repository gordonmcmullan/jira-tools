"""
Format, as human readable text, completed issues for a specified Jira project
"""
from config import Config



class Summary():

    FIELDS = "Summary"

class WeeklyThroughput():

    FIELDS = "Summary"

    @staticmethod
    def number_to_text(number: int) -> str:
        numbers = [
            "zero", "one", "two", "three", "four", "five", "six", "seven",
            "eight", "nine", "ten", "eleven", "twelve"
        ]
        return numbers[number]

    @staticmethod
    def completed_for_week(config: Config, jira, weeks_ago: int) -> str:

        preamble = "Last week " if weeks_ago == 0 else f"{WeeklyThroughput.number_to_text(weeks_ago + 1).title()} weeks ago "
        issues = jira.search_issues(
            f"project={config.project} \
                AND issuetype in (Story, Task) \
                AND status in (Done, Closed) \
                AND resolutionDate <  startOfWeek(-{weeks_ago}w) \
                AND resolutionDate >= startOfWeek(-{weeks_ago + 1}w)",
            fields="summary"
        )
        return preamble + str(issues.total)
