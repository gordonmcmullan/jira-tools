# jira-tools
Useful CLI tool for interacting with JIRA instances through python

## Usage

`python3 jira_tools.py action -p PROJECT [-j <jira_url>] [-w <weeks>]`

Provides some basic functionality to connect to Jira and extract information for analysis of Jira project issues.

Reads connection credentials from the users .netrc which should contain a machine entry like the following:

```text
machine <jirahost>
    login <username>
    password <password>
```

### Required Arguments
    
`action <issue_history | weekly_throughput >`

| action | description |
| --- | --- |
| `issue_history` | print issues transition details as plain text output to stdout |
| `weekly_throughput` | export weekly throughput of Stories and Tasks for the last `<n>` weeks (default n = 4) |
| | |

`-p|--project PROJECT` the jira project id

### Optional Arguments

`-h|--help` Print a help message and exit

`-j|--jira <jira_url>` url of the JIRA instance to connect to, defaults to "http://localhost:2990/" which is the url used by the Development JIRA from the Atlassian SDK

`-w|--weeks <weeks>` number of weeks to count back, defaults to four weeks

## Examples

Here are some examples of the actions available and the output they create

### Issue History

```python3 jira_tools.py issue_history -p PROJECT -j <jira_url>```

```text
Running jira-tools

 PROJECT-39 Bug
         25/07/2019 09:31 Created
         26/07/2019 04:03 Status In Progress
         26/07/2019 04:03 Status Review
         29/07/2019 04:03 Status Done

 PROJECT-38 Story
         22/05/2019 04:43 Created
         17/06/2019 08:12 Status Backlog
         17/06/2019 08:19 Status To Do
         18/06/2019 05:09 Status Ready
         23/06/2019 11:27 Status In Progress
         05/07/2019 03:25 Flagged Impediment
         10/07/2019 04:04 Unflagged
         11/07/2019 03:10 Status Review
         11/07/2019 03:14 Status Done

 PROJECT-113 Task
         11/07/2019 07:04 Created
         11/07/2019 07:05 Status In Progress
         22/07/2019 11:20 Flagged Impediment
         25/07/2019 03:13 Unflagged
         25/07/2019 08:15 Status Review
         26/07/2019 03:38 Status Done
```

### Weekly Throughput

```python3 jira_tools.py weekly_throughput -w 6 -p PROJECT -j <jira_url>```

```text
Running jira-tools
Total stories completed to date: 33
Completed stories so far this week 1
weekly totals for the last 6 weeks
Last week  10
Two weeks ago 3
Three weeks ago 6
Four weeks ago 7
Five weeks ago 1
Six weeks ago 2
```
