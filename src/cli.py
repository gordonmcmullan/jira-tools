"""Command line API handling for jira-tools"""
import argparse
import sys
#pylint: disable=too-few-public-methods missing-function-docstring
class Colour:
    """ Enumeration for modifying the colours used in the terminal output"""
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

def argument_parser() -> argparse.ArgumentParser:
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
        usage="jira_tools.py action -p PROJECT [-j JIRA] [-w WEEKS]",
        add_help=False
    )

    required_args = parser.add_argument_group('required arguments')
    optional_args = parser.add_argument_group('optional arguments')

    required_args.add_argument(
        "action",
        default="text",
        nargs="?",
        help="Which action to perform:\n" +
        Colour.BOLD + "\nissue_history" + Colour.END +
        " export issues as plain text output to stdout (default)\n" +
        Colour.BOLD + "\nweekly_throughput" + Colour.END +
        " export data to help forecast\n\n\n"
    )

    required_args.add_argument(
        "-p",
        "--project",
        help="the jira project name",
        required=True
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

def exit_script(parser: argparse.ArgumentParser) -> None:
    print("\nError: Invalid action given\n")
    parser.print_help()
    sys.exit(1)
