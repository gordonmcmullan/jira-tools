"""output of all issues in csv format for a specified Jira project"""
import iso8601
from jira import Issue
from iso8601 import parse_date
import filters

class CsvAllIssues():
    """
    Class CsvAllIssues
    Functions and Constants used to select and format all issues for a
    specified Jira project
    """
    HEADER = "\"Issue Type\",IssueKey,IssueId,Summary,Status,Resolution,Created,Updated,Resolved,\"Epic Link\",Started,Completed"

    FIELDS = "changelog, issuetype, summary, status, resolution, created, updated, resolutiondate, customfield_10008"
    EXPAND = "changelog"

    @staticmethod
    def generate_jql(config):
        """Given a config object return the JQL string to select the appropriate issues"""
        return  f"project={config.project} AND issuetype NOT IN (Epic) ORDER by issueKey ASC"

    @staticmethod
    def format_issue(issue : Issue) -> str:
        "Format an individual issue as a series of lines of csv"

        resolution = issue.fields.resolution.name if issue.fields.resolution is not None else ""
        resolutiondate = issue.fields.resolutiondate if issue.fields.resolutiondate is not None else ""

        formatted_issue = ""
        formatted_issue += f"{issue.fields.issuetype.name},{issue.key},{issue.id},\"{issue.fields.summary}\""
        formatted_issue += f",{issue.fields.status.name}"
        formatted_issue += f",{resolution}"
        formatted_issue += f",\"{parse_date(issue.fields.created).strftime('%d/%m/%Y %H:%M')}\""
        formatted_issue += f",\"{parse_date(issue.fields.updated).strftime('%d/%m/%Y %H:%M')}\""
        formatted_issue += f",\"{parse_date(resolutiondate).strftime('%d/%m/%Y %H:%M')}\""
        formatted_issue += f",{issue.fields.customfield_10008}"

        histories = issue.changelog.histories
        start_found = False
        done_time = ""
        closed_time = ""

        for history in histories:
            timestamp = iso8601.parse_date(history.created)
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
