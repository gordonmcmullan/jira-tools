"""output of completed issues in csv format for a specified Jira project"""
from jira import Issue
from iso8601 import parse_date

import filters

class CSV():
    """
    Class CSV
    Functions and Constants used to select and format completed issues for a
    specified Jira project
    """
    HEADER = "issueKey,\"Epic Link\",summary,created,started,completed"

    FIELDS = "changelog, created, summary, status, issuetype, customfield_10008"
    EXPAND = "changelog"

    @staticmethod
    def generate_jql(config):
        return  f"project={config.project} \
                AND issuetype NOT IN (Epic) \
                AND status IN (Done, Closed) \
                AND status changed TO (Done, Closed) \
                AFTER startOfWeek(-{config.weeks}w)"

    @staticmethod
    def format_issue(issue: Issue)-> str:
        "Format an individual issue as a series of lines of csv"
        formatted_issue = ""
        formatted_issue += f"{issue.key}"
        formatted_issue += f",{issue.fields.customfield_10008}"
        formatted_issue += f",\"{issue.fields.summary}\""
        formatted_issue += f",\"{parse_date(issue.fields.created).strftime('%d/%m/%Y %H:%M')}\""

        histories = issue.changelog.histories
        start_found = False
        done_time = ""
        closed_time = ""

        for history in histories:
            timestamp = parse_date(history.created)
            transitions = filter(filters.is_transition, history.items)
            for transition in transitions:
                if not start_found and filters.is_in_progress(transition):
                    formatted_issue += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                    start_found = True
                if filters.is_complete(transition):
                    if start_found is False:
                        formatted_issue += ","
                        # include only one 'missing' to "In Progress" timestamp
                        start_found = True
                    if transition.toString.lower == "done":
                        done_time = f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                    else:
                        closed_time = f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
        if done_time:
            formatted_issue += done_time
        else:
            formatted_issue += closed_time

        return formatted_issue
