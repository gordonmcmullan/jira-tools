"""
Some useful tools to interact with JIRA instances
"""
import argparse
import iso8601
import json
from jira import JIRA


class Config:
    """ Config - contains useful configuration settings """
    def __init__(self,
                 project,
                 jira_url: str,
                 weeks: int = 4):
        self.args = []
        self.jira = JIRA(jira_url) if jira_url != "" else JIRA("http://localhost:2990/")
        self.project = project
        self.weeks = weeks


class Colour:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def number_to_text(number: int):
    numbers = [
        "zero", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve"
        ]
    return numbers[number]


def main():
    """ main thread """
    parser = argument_parser()
    args = vars(parser.parse_args())
    config = Config(args['project'], args['jira'], args['weeks'])

    print("Running jira-tools")
    action = globals()[args['action']]

    action(config)

    config.jira.close()


def text(config: Config) -> None:
    jira = config.jira
    print(jira.client_info())


def issue_history(config: Config) -> None:
    jira = config.jira

    issues = jira.search_issues(
        f"project={config.project} AND status=Done",
        fields="changelog, created, status, issuetype",
        expand="changelog"
    )

    for issue in issues:
        print(
            "\n",
            issue.key,
            issue.fields.issuetype.name,
            "\n\t",
            iso8601.parse_date(
                issue.fields.created).strftime('%d/%m/%Y %H:%M'),
            "Created"
        )
        histories = issue.changelog.histories
        for history in histories:
            timestamp = iso8601.parse_date(history.created)
            items = history.items
            for item in items:
                if item.field.lower() in ["status", "flagged"]:
                    if item.toString == "":
                        title = "Unflagged"
                    else:
                        title = item.field.title()
                    print(
                        "\t",
                        timestamp.strftime('%d/%m/%Y %H:%M'),
                        title,
                        item.toString
                    )


def weekly_throughput(config: Config):
    jira = config.jira

    issues = jira.search_issues(
        f"project={config.project} \
          AND status=Done \
          AND issuetype in (Story, Task)",
        fields="summary"
    )
    print(f"Total stories completed to date: {issues.total}")

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
        pass


def argument_parser():
    parser = argparse.ArgumentParser(
        description="Provides some basic functionality to "
        "connect to Jira and extract "
        "information for analysis of Jira project issues.\n\n"
        "Reads connection credentials from the users .netrc which should "
        "contain a machine entry like the following:"
        "\n\n"
        "\tmachine <jirahost>\n"
        "\t  login <username>\n"
        "\t  password <password>",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    
    required_args = parser.add_argument_group('required arguments')
    optional_args = parser.add_argument_group('optional arguments')

    parser.add_argument(
        "action",
        default="text",
        nargs="?",
        help="Which action to perform:\n" +
             Colour.BOLD + "\ntext" + Colour.END +
             " export issues as plain text output to stdout (default)\n" +
             Colour.BOLD + "issue_history" + Colour.END +
             " export data to help forecast\n"
    )

    required_args.add_argument(
        "-p",
        "--project",
        help="the jira project name"
    )

    optional_args.add_argument(
        "-h",
        "--help",
        help="Print this message and exit\n\n",
        action="help"
    )

    optional_args.add_argument(
        "-j",
        "--jira",
        help="url of the JIRA instance to connect to,\n"
             "defaults to \"http://localhost:2990/\"\n"
             "which is the url used by the Development JIRA "
             "from the Atlassian SDK\n\n",
        required=False
    )

    optional_args.add_argument(
        "-w",
        "--weeks",
        help="number of weeks to count back,\n"
             "defaults to four weeks\n\n",
        required=False,
        type=int
    )

    return parser


if __name__ == "__main__":
    main()
