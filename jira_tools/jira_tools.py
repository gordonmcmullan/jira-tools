#!/usr/bin/env python3
"""
Some useful Commandline tools to interact with JIRA instances
"""
#import argparse
import time
import iso8601
from jira import JIRA

from cli import argument_parser, exit_script

class Config:
    """ Config - contains useful configuration settings """
    def __init__(self,
                 project: str,
                 jira_url: str,
                 weeks: int) -> None:
        self.args = []

        self.project = project

        if jira_url != "":
            self.jira = JIRA(jira_url)
        else:
            self.jira = JIRA("http://localhost:2990/")

        if weeks:
            assert 0 <= weeks <= 13
            self.weeks = weeks
        else:
            self.weeks = 4

class actions:

    ALLOWED_ACTIONS = ["issue_history", "weekly_throughput", "text", "csv"]


def number_to_text(number: int) -> str:
    numbers = [
        "zero", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve"
    ]
    return numbers[number]


def main() -> None:
    """ main thread """
    parser = argument_parser()
    args = vars(parser.parse_args())
    if args['action'] not in actions.ALLOWED_ACTIONS:
        exit_script(parser)
    try:
        action = globals()[args['action']]
    except KeyError:
        exit_script(parser)
    if callable(action):
        config = Config(args['project'], args['jira'], args['weeks'])
        action(config)
    else:
        exit_script(parser)
    config.jira.close()


def text(config: Config) -> None:
    jira = config.jira
    print(jira.client_info())

def csv(config: Config) -> None:
    jira = config.jira

    issues = get_issues_by_jql(
        jira = jira,
        jql = f"project={config.project} \
                AND issuetype NOT IN (Epic) \
                AND status IN (Done, Closed) \
                AND status changed TO (Done, Closed) \
                AFTER startOfWeek(-{config.weeks}w)",
        fields="changelog, created, summary, status, issuetype, customfield_10008",
        expand="changelog"
    )
    print("issueKey,\"Epic Link\",summary,created,started,completed")
    for issue in issues:
        done_time = ""
        closed_time = ""
        formatted_issue = ""
        formatted_issue += f"{issue.key}"
        formatted_issue += f",{issue.fields.customfield_10008}"
        formatted_issue += f",\"{issue.fields.summary}\""
        formatted_issue += f",\"{iso8601.parse_date(issue.fields.created).strftime('%d/%m/%Y %H:%M')}\""
        
        histories = issue.changelog.histories
        start_found = False
        for history in histories:
            timestamp = iso8601.parse_date(history.created)
            transitions = filter(is_transition, history.items)
            for transition in transitions:
                if not start_found and is_in_progress(transition):
                    formatted_issue += f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                    start_found = True            
                if is_complete(transition):
                    if start_found is False:
                        formatted_issue +=","
                        start_found = True # ToDo: just a hack to give us only one 'missing' to "In Progress" timestamp
                    if transition.toString.lower == "done":
                        done_time = f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
                    else:
                        closed_time = f",\"{timestamp.strftime('%d/%m/%Y %H:%M')}\""
        if done_time:    
            formatted_issue += done_time
        else:
            formatted_issue += closed_time
        
        print(formatted_issue)


def issue_history(config: Config) -> None:
    print("Running jira-tools\n\n")

    jira = config.jira

    issues = get_issues_by_jql(
        jira=jira,
        jql=f"project={config.project} \
            AND issuetype NOT IN (Epic) \
            AND status IN (Done, Closed) \
            AND status changed TO (Done, Closed) \
            AFTER startOfWeek(-{config.weeks}w)",
        fields="changelog, summary, created, status, issuetype, customfield_10008",
        expand="changelog"
    )

    for issue in issues:
        print(format_issue(issue))


        histories = issue.changelog.histories
        for history in histories:
            timestamp = iso8601.parse_date(history.created)
            transitions = filter(is_transition, history.items)
            for transition in transitions:
                transition_string = format_transition(transition, timestamp)
                print(transition_string)


def get_issues_by_jql(
        jira: JIRA, jql: str, fields: str, expand: str) -> JIRA.issue:
    start_at = 0
    has_more = True
    while has_more:
        issues = jira.search_issues(
            jql, startAt=start_at, fields=fields, expand=expand)
        for issue in issues:
            yield issue
        start_at += len(issues)
        if len(issues) < issues.maxResults:
            has_more = False
        else:
            time.sleep(1)  # play nicely with API

def format_issue(issue: object) -> str:
    formatted_issue = ""
    formatted_issue += f"\n[Epic: {issue.fields.customfield_10008}]\n"
    formatted_issue += f"{issue.fields.issuetype.name} : "
    formatted_issue += f"{issue.key} {issue.fields.summary}\n"
    formatted_issue += f"\t {iso8601.parse_date(issue.fields.created).strftime('%d/%m/%Y %H:%M')} Created" 
    return formatted_issue

def format_transition(transition: object, timestamp: str) -> str:
    if transition.toString == "": # toString here is a property representing the Name of the status transitioned to
        title = "Unflagged"
    else:
        title = transition.field.title()
    return f"\t {timestamp.strftime('%d/%m/%Y %H:%M')} {title} {transition.toString}"

def is_transition(item) -> bool:
    return item.field.lower() in ["status", "flagged"]

def is_in_progress(item) -> bool:
    return item.toString is not None and item.toString.lower() == "in progress"
   
def is_complete(item) -> bool:
    return item.toString is not None and item.toString.lower() in ["done", "closed"]


def weekly_throughput(config: Config) -> None:
    jira = config.jira

    issues = jira.search_issues(
        f"project={config.project} \
          AND status in (Done) \
          AND issuetype in (Story, Task)",
        fields="summary"
    )
    print(f"Total stories {Colour.GREEN}Done{Colour.END} to date: {issues.total}")

    issues = jira.search_issues(
    f"project={config.project} \
        AND status in (Closed) \
        AND issuetype in (Story, Task)",
    fields="summary"
    )
    print(f"Total stories {Colour.RED}Closed{Colour.END} to date: {issues.total}")

    issues = jira.search_issues(
    f"project={config.project} \
        AND status in (Done, Closed) \
        AND issuetype NOT IN (Epic)",
    fields="summary"
    )
    print(f"Total stories with {Colour.YELLOW}no ResolutionDate{Colour.END} to date: {issues.total}")

    issues = jira.search_issues(
        f"project={config.project} \
            AND issuetype in (Story, Task) \
            AND status = Done \
            AND resolutiondate >= startOfWeek()",
        fields="summary"
        )
    print(f"Completed stories so far this week {issues.total}")

    print(f"weekly totals for the last {config.weeks} weeks")
    for week in range(0, config.weeks):
        if week == 0:
            preamble = "Last week "
        else:
            preamble = f"{number_to_text(week + 1).title()} weeks ago"

        issues = jira.search_issues(
            f"project={config.project} \
                AND issuetype in (Story, Task) \
                AND status = Done \
                AND resolutiondate <  startOfWeek(-{week}w) \
                AND resolutiondate >= startOfWeek(-{week + 1}w)",
            fields="summary"
        )
        print(preamble, issues.total)


def monte_carlo(config: Config) -> None:
    jira = config.jira

    print(f"running monte carlo simulation with {config.rounds}")
    issues = jira.search_issues(
        f"project={config.project} AND status=Done",
        fields="changelog, created, status, issuetype",
        expand="changelog"
    )
    for issue in issues:
        print(issue.key)


if __name__ == "__main__":
    main()
