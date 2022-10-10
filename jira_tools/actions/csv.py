import iso8601
import filters
from jira import Issue


class CSV():
    
    HEADER = "issueKey,\"Epic Link\",summary,created,started,completed"

    FIELDS = "changelog, created, summary, status, issuetype, customfield_10008"
    EXPAND = "changelog"

    def generate_jql(config):
        return  f"project={config.project} \
                AND issuetype NOT IN (Epic) \
                AND status IN (Done, Closed) \
                AND status changed TO (Done, Closed) \
                AFTER startOfWeek(-{config.weeks}w)"
    
    @staticmethod
    def format_issue(issue: Issue)-> str:
        formatted_issue = ""
        formatted_issue += f"{issue.key}"
        formatted_issue += f",{issue.fields.customfield_10008}"
        formatted_issue += f",\"{issue.fields.summary}\""
        formatted_issue += f",\"{iso8601.parse_date(issue.fields.created).strftime('%d/%m/%Y %H:%M')}\""

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
                        # ToDo: just a hack to give us only one 'missing' to "In Progress" timestamp
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
