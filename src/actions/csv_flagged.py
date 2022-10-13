"""output of flagged and Unflagged events in csv format for a specified Jira project"""
from jira import Issue
import iso8601

import filters

class CsvFlagged():
    """
    Class CsvFlagged
    Functions and Constants used to select and format completed issues
    which were flaged during their lifetime for a specified Jira project
    """
    HEADER = "issueKey,issuedId,Summary,\"Epic Link\",flagged,unflagged"

    FIELDS = "changelog, created, summary, status, issuetype, customfield_10008"
    EXPAND = "changelog"


    @staticmethod
    def generate_jql(config):
        """Create the required JQL statement to seach for the required issues"""
        return  f"project={config.project} \
                AND issuetype NOT IN (Epic) \
                AND status IN (Done, Closed) \
                AND status changed TO (Done, Closed) \
                AFTER startOfWeek(-{config.weeks}w) \
                ORDER by issueKey ASC"


    @staticmethod
    def format_issue(issue: Issue)-> str:
        """format a signle issue into zero or more CSV lines where an issue was flagged and unflagged"""
        histories = issue.changelog.histories
        formatted_issue = ""
        for history in histories:
            timestamp = iso8601.parse_date(history.created)
            flags = filter(filters.is_flag, history.items)
            for flag in flags:
                if flag.toString not in ("", None):
                    formatted_issue += f"{issue.key}"
                    formatted_issue += f",{issue.id}"
                    formatted_issue += f",\"{issue.fields.summary}\""
                    formatted_issue += f",{issue.fields.customfield_10008}"
                    formatted_issue += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                else:
                    formatted_issue += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\"\n"
        return formatted_issue
