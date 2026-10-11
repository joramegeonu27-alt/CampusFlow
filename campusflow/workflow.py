"""Ticket assignment, status management, and work queue."""


PRIORITY_ORDER = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}


def find_ticket(tickets, ticket_id):
    """Find a ticket or raise an error if it does not exist."""

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Please enter a valid ticket ID.")

    ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket["id"].upper() == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} was not found.")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a staff member."""

    ticket = find_ticket(tickets, ticket_id)

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name cannot be blank.")

    if ticket["status"] == "resolved":
        raise ValueError(
            "This ticket is resolved. Reopen it before making changes."
        )

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def change_status(tickets, ticket_id, new_status):
    """Move a ticket through the required workflow."""

    ticket = find_ticket(tickets, ticket_id)

    if not isinstance(new_status, str):
        raise ValueError("Status must be open, in_progress, or resolved.")

    new_status = new_status.strip().lower()

    allowed_statuses = ["open", "in_progress", "resolved"]

    if new_status not in allowed_statuses:
        raise ValueError(
            "Status must be open, in_progress, or resolved."
        )

    current_status = ticket["status"]

    if current_status == "resolved":
        raise ValueError(
            "Resolved tickets must be reopened before they can be changed."
        )

    if current_status == new_status:
        raise ValueError(
            f"Ticket {ticket['id']} is already {current_status}."
        )

    if current_status == "open" and new_status == "in_progress":

        if not ticket["assigned_to"]:
            raise ValueError(
                "Assign this ticket to a staff member before starting work."
            )

        ticket["status"] = "in_progress"
        return ticket

    if current_status == "in_progress" and new_status == "resolved":

        ticket["status"] = "resolved"
        return ticket

    raise ValueError(
        f"Invalid status change: {current_status} to {new_status}."
    )


def update_status(tickets, ticket_id, new_status):
    """Update status using the function name expected by main.py."""

    return change_status(tickets, ticket_id, new_status)


def reopen_ticket(tickets, ticket_id):
    """Reopen a resolved ticket."""

    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"

    return ticket


def get_work_queue(tickets):
    """Return unresolved tickets ordered by priority and numeric ID."""

    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] != "resolved"
    ]

    def sort_key(ticket):
        ticket_id = ticket["id"]
        numeric_id = int(ticket_id[1:]) if ticket_id[1:].isdigit() else float("inf")

        return (
            PRIORITY_ORDER.get(ticket["priority"], 99),
            numeric_id,
        )

    return sorted(unresolved_tickets, key=sort_key)