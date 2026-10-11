"""Generate CampusFlow ticket reports."""


STATUSES = ["open", "in_progress", "resolved"]

PRIORITIES = ["critical", "high", "medium", "low"]


def generate_report(tickets):
    """Generate a report compatible with main.py."""

    by_status = {
        status: 0
        for status in STATUSES
    }

    by_priority = {
        priority: 0
        for priority in PRIORITIES
    }

    for ticket in tickets:

        status = ticket["status"]
        priority = ticket["priority"]

        if status in by_status:
            by_status[status] += 1

        if priority in by_priority:
            by_priority[priority] += 1

    return {
        "total_tickets": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }