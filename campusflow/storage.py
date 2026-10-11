"""Save and load CampusFlow tickets using JSON."""

import json
from pathlib import Path

from campusflow.tickets import calculate_priority


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "tickets.json"
)


def load_tickets(path=None):
    """Load saved tickets or return an empty list if the file is missing."""

    file_path = Path(path) if path is not None else DATA_FILE

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Saved ticket file contains invalid JSON: {error}"
        ) from error

    except OSError as error:
        raise OSError(
            f"Could not read saved tickets: {error}"
        ) from error

    if not isinstance(tickets, list):
        raise ValueError("Saved ticket data must be a list.")

    seen_ids = set()

    required_fields = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
    }

    for ticket in tickets:

        if not isinstance(ticket, dict):
            raise ValueError("Every saved ticket must be an object.")

        if not required_fields.issubset(ticket.keys()):
            raise ValueError("A saved ticket is missing required fields.")

        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str):
            raise ValueError("A saved ticket has an invalid ID.")

        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID found: {ticket_id}")

        seen_ids.add(ticket_id)

        if not ticket_id.startswith("T") or not ticket_id[1:].isdigit():
            raise ValueError(f"Invalid ticket ID: {ticket_id}")

        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise ValueError("A saved ticket has an invalid title.")

        if ticket["status"] not in ["open", "in_progress", "resolved"]:
            raise ValueError(f"Invalid status in ticket {ticket_id}.")

        if ticket["assigned_to"] is not None:
            if (
                not isinstance(ticket["assigned_to"], str)
                or not ticket["assigned_to"].strip()
            ):
                raise ValueError(
                    f"Invalid staff assignment in ticket {ticket_id}."
                )

        try:
            expected_priority = calculate_priority(
                ticket["urgency"],
                ticket["affected_users"],
            )
        except (ValueError, TypeError) as error:
            raise ValueError(
                f"Invalid ticket data for {ticket_id}: {error}"
            ) from error

        if ticket["priority"] != expected_priority:
            raise ValueError(
                f"Incorrect priority stored for ticket {ticket_id}."
            )

    return tickets


def save_tickets(tickets, path=None):
    """Save tickets to the JSON file."""

    file_path = Path(path) if path is not None else DATA_FILE

    file_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = file_path.with_suffix(file_path.suffix + ".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4, ensure_ascii=False)
            file.write("\n")

        temporary_file.replace(file_path)

    except (OSError, TypeError, ValueError) as error:

        if temporary_file.exists():
            temporary_file.unlink()

        raise OSError(
            f"Could not save tickets: {error}"
        ) from error