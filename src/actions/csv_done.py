"""output of completed issues in csv format for a specified Jira project"""
from jira import Issue
from iso8601 import parse_date

import filters

class CsvDone():
    """
    Class CsvDone
    Functions and Constants used to select and format completed issues for a
    specified Jira project
    """
    # pylint: disable=line-too-long
    HEADER = "\"Issue Type\",\"Issue Key\",\"Issue id\",Summary,Assignee,Reporter,Prioity,Status,Resolution,Created,Updated,Epic,TIP,start,complete"

    FIELDS = "changelog, issuetype, issuekey, id, summary, assignee, reporter, priority, status, resolution, created, updated, customfield_10008"
    EXPAND = "changelog"


    @staticmethod
    def generate_jql(config):
        return  f"project={config.project} \
                AND issuetype NOT IN (Epic) \
                AND status IN (Done, Closed) \
                AND status changed TO (Done, Closed) \
                AFTER startOfWeek(-{config.weeks}w)"

    @staticmethod
    def format_issue(issue: Issue, row: int)-> str:
        "Format an individual issue as a series of lines of csv"
        formatted_issue = ""
        formatted_issue += f"{issue.fields.issuetype.name}"
        formatted_issue += f",{issue.key}"
        formatted_issue += f",{issue.id}"
        formatted_issue += f",\"{issue.fields.summary}\""
        formatted_issue += f",\"{issue.fields.assignee.name}\"" if issue.fields.assignee else ","
        formatted_issue += f",\"{issue.fields.reporter.name}\""
        formatted_issue += f",\"{issue.fields.priority.name}\""
        formatted_issue += f",\"{issue.fields.status.name}\""
        formatted_issue += f",\"{issue.fields.resolution.name}\"" if issue.fields.resolution else ","
        formatted_issue += f",\"{parse_date(issue.fields.created).strftime('%d/%m/%Y %H:%M')}\""
        formatted_issue += f",\"{parse_date(issue.fields.updated).strftime('%d/%m/%Y %H:%M')}\""
        formatted_issue += f",{issue.fields.customfield_10008}"
        formatted_issue += f",\"=NETWORKDAYS(N{row},O{row})\""


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
                    if transition.toString.lower == "done":
                        done_time = ""
                        if not start_found: done_time += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                        done_time += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                        start_found = True
                    else:
                        closed_time = ""
                        if not start_found: closed_time += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                        closed_time += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
        if done_time:
            formatted_issue += done_time
        else:
            formatted_issue += closed_time

        return formatted_issue
