"""Factory to create test jira Issues from json"""
from jira import Issue

default_dict = {
            "key" : "PROJECT-1",
            "id" : "00001",
            "fields" : {
                "created" : "2022-01-01T00:00:00.000+00:00",
                "summary" : "Issue Summary",
                "customfield_10008" : "EPIC-1",
                "issuetype" : {
                    "name" : "Issue"
                }}, # fields
            "changelog" : {
                "histories" : [{
                    "created" : "2022-01-02T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "In Progress",
                      "field" : "status" }]
                },{
                    "created" : "2022-01-03T00:00:00.000+00:00",
                    "items" : [
                    { "toString" : "Done",
                      "field" : "status" }]
                }] # histories
            } # changelog
        } # fromDict

def started_json(timestamp) -> dict:
    return {"created" : timestamp, "items" : [{ "toString" : "In Progress","field" : "status" }]}

def create_test_issue(raw_dict: dict = None) -> Issue:
    if raw_dict is None:
        raw_dict = dict(default_dict)
    return Issue(options=None, session=None, raw=raw_dict)
