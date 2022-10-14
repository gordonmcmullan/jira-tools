# pylint: disable=missing-function-docstring,missing-module-docstring

def is_transition(item) -> bool:
    return item.field.lower() in ["status", "flagged"]

def is_flag(item) -> bool:
    return item.field.lower() == "flagged"

def is_in_progress(item) -> bool:
    return item.toString is not None and item.toString.lower() == "in progress"

def is_complete(item) -> bool:
    return item.toString is not None and item.toString.lower() in ["done", "closed"]
