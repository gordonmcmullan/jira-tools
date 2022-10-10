#!/usr/bin/env python3
"""
Some useful Commandline tools to interact with JIRA instances
"""
import time
from jira import JIRA

from cli import argument_parser, Actions, Colour, exit_script
from config import Config
from actions import CSV, CsvAllIssues, CsvFlagged, IssueHistory

def main() -> None:
    """ main thread """
    parser = argument_parser()
    args = vars(parser.parse_args())
    if args['action'] not in Actions.ALLOWED_ACTIONS:
        exit_script(parser)
    try: # ToDo clean this up
        action = globals()[args['action']]
    except KeyError:
        exit_script(parser)
    if callable(action):
        config = Config(args['project'], args['jira'], args['weeks'])
        action(config)
    else:
        exit_script(parser)
    config.jira.close()

#ToDo: Extract this
def get_issues_by_jql(jira: JIRA, jql: str, fields: str, expand: str):
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

def number_to_text(number: int) -> str:
    numbers = [
        "zero", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve"
    ]
    return numbers[number]

def text(config: Config) -> None:
    jira = config.jira
    print(jira.client_info())


def csv(config: Config) -> None:
    issues = get_issues_by_jql(
        jira = config.jira,
        jql = CSV.generate_jql(config),
        fields=CSV.FIELDS,
        expand=CSV.EXPAND
    )
    print(CSV.HEADER)
    for issue in issues:
        print(CSV.format_issue(issue))


def csv_all_issues(config: Config) -> None:
    issues = get_issues_by_jql(
        jira = config.jira,
        jql = CsvAllIssues.generate_jql(config),
        fields=CsvAllIssues.FIELDS,
        expand = CsvAllIssues.EXPAND
    )    
    print(CsvAllIssues.HEADER)    
    for issue in issues:
        print(CsvAllIssues.format_issue(issue))


def csv_flagged(config: Config) -> None:
    issues = get_issues_by_jql(
        jira = config.jira,
        jql = CsvFlagged.generate_jql(config),
        fields = CsvFlagged.FIELDS,
        expand = CsvFlagged.EXPAND
    )
    print(CsvFlagged.HEADER)
    for issue in issues:
        print(CsvFlagged.format_issue(issue), end="") 


def issue_history(config: Config) -> None:
    issues = get_issues_by_jql(
        jira=config.jira,
        jql = IssueHistory.generate_jql(config),
        fields=IssueHistory.FIELDS,
        expand=IssueHistory.EXPAND
    )
    for issue in issues:
        print(IssueHistory.format_issue(issue))

#ToDo Extract to actions
def weekly_throughput(config: Config) -> None:
    jira = config.jira

    issues = jira.search_issues(
        f"project={config.project} \
          AND status in (Closed, Done) \
          AND issuetype in (Story, Task) \
          AND resolution = Done",
        fields="summary"
    )
    print(f"Total stories {Colour.GREEN}Done{Colour.END} to date: {issues.total}")

    issues = jira.search_issues(
    f"project={config.project} \
        AND status in (Done, Closed) \
        AND issuetype in (Story, Task)",
    fields="summary"
    )
    print(f"Total stories {Colour.RED}Closed{Colour.END} to date: {issues.total}")
 
    issues = jira.search_issues(
    f"project={config.project} \
        AND status in (Done, Closed) \
        AND issuetype NOT IN (Epic) \
        AND resolutionDate is Empty",
    fields="summary"
    )
    print(f"Total stories without {Colour.YELLOW}resolutionDate{Colour.END} to date: {issues.total}")

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
                AND status in (Done, Closed) \
                AND resolutionDate <  startOfWeek(-{week}w) \
                AND resolutionDate >= startOfWeek(-{week + 1}w)",
            fields="summary"
        )
        print(preamble, issues.total)

#ToDo: extract to actions and complete
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
