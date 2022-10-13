"""
Format, as human readable text, completed issues for a specified Jira project
"""
from datetime import datetime
import iso8601
from jira import Issue

import filters

class IssueHistory():

    FIELDS = "changelog, summary, created, status, issuetype, customfield_10008"
    EXPAND = "changelog"

    @staticmethod
    def generate_jql(config):
        return  f"project={config.project} \
                AND issuetype NOT IN (Epic) \
                AND status IN (Done, Closed) \
                AND status changed TO (Done, Closed) \
                AFTER startOfWeek(-{config.weeks}w)"

    @staticmethod
    def format_transition(transition: object, timestamp: datetime) -> str:
        if transition.toString == "":  # toString is a property representing the Name of the status transitioned to
            title = "Unflagged"
        else:
            title = transition.field.title()
        return f"\t {timestamp.strftime('%d/%m/%Y %H:%M')} {title} {transition.toString}"

    @staticmethod
    def format_issue(issue: Issue) -> str:
        formatted_issue = ""
        formatted_issue += f"\n[Epic: {issue.fields.customfield_10008}]\n"
        formatted_issue += f"{issue.fields.issuetype.name} : "
        formatted_issue += f"{issue.key} {issue.fields.summary}\n"
        formatted_issue += f"\t {iso8601.parse_date(issue.fields.created).strftime('%d/%m/%Y %H:%M')} Created\n"

        histories = issue.changelog.histories
        for history in histories:
            timestamp = iso8601.parse_date(history.created)
            transitions = filter(filters.is_transition, history.items)
            for transition in transitions:
                transition_string = IssueHistory.format_transition(
                    transition, timestamp)
                formatted_issue += transition_string + "\n"

        return formatted_issue
