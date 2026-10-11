"""Ticket creation, validation, and priority calculation."""


CATEGORIES = ["Network", "Hardware", "Software", "Other"]

URGENCY_LEVELS = ["low", "medium", "high"]

PRIORITIES = ["critical", "high", "medium", "low"]

STATUSES = ["open", "in_progress", "resolved"]


def normalize_category(category):
    """Validate a category and return its standard spelling."""

    if not isinstance(category, str):
        raise ValueError("Category must be text.")

    category = category.strip().lower()

    for valid_category in CATEGORIES:
        if category == valid_category.lower():
            return valid_category

    raise ValueError(
        "Invalid category. Choose Network, Hardware, Software, or Other."
    )


def normalize_urgency(urgency):
    """Validate urgency and convert it to lowercase."""

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")

    urgency = urgency.strip().lower()

    if urgency not in URGENCY_LEVELS:
        raise ValueError("Urgency must be low, medium, or high.")

    return urgency


def validate_affected_users(affected_users):
    """Require a positive whole number."""

    if type(affected_users) is not int:
        raise ValueError("Affected users must be a whole number.")

    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return affected_users


def calculate_priority(urgency, affected_users):
    """Calculate priority using the assessment's required rules."""

    urgency = normalize_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def next_ticket_id(tickets):
    """Generate a unique sequential ticket ID."""

    highest_id = 0

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            number = ticket_id[1:]

            if number.isdigit():
                highest_id = max(highest_id, int(number))

    return f"T{highest_id + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate and create a new ticket."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be blank.")

    category = normalize_category(category)
    urgency = normalize_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    priority = calculate_priority(urgency, affected_users)

    ticket = {
        "id": next_ticket_id(tickets),
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)

    return ticket


def list_tickets(tickets):
    """Return all tickets."""

    return list(tickets)


def get_ticket(tickets, ticket_id):
    """Find a ticket by ID, returning None if it does not exist."""

    if not isinstance(ticket_id, str):
        return None

    ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket.get("id", "").upper() == ticket_id:
            return ticket

    return None