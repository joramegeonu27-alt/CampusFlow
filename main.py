import sys

from campusflow.tickets import create_ticket, list_tickets, get_ticket
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import generate_report


def display_menu():
    print("\n" + "=" * 45)
    print("           CAMPUSFLOW HELPDESK")
    print("=" * 45)
    print("1. Create a new ticket")
    print("2. List all tickets")
    print("3. View ticket details")
    print("4. Assign ticket to staff")
    print("5. Update ticket status")
    print("6. View work queue")
    print("7. Generate reports")
    print("8. Save tickets")
    print("9. Exit")
    print("=" * 45)


def create_new_ticket(tickets):
    print("\n--- CREATE NEW TICKET ---")

    title = input("Enter ticket title: ").strip()
    category = input(
        "Enter category (Network, Hardware, Software, Other): "
    ).strip()

    urgency = input(
        "Enter urgency (low, medium, high): "
    ).strip()

    affected_users = input(
        "Enter number of affected users: "
    ).strip()

    try:
        affected_users = int(affected_users)

        ticket = create_ticket(
            tickets,
            title,
            category,
            urgency,
            affected_users,
        )

        print("\nTicket created successfully!")
        print(f"Ticket ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")

    except (ValueError, TypeError) as error:
        print(f"\nError: {error}")


def show_all_tickets(tickets):
    print("\n--- ALL TICKETS ---")

    if not tickets:
        print("No tickets have been created yet.")
        return

    for ticket in list_tickets(tickets):
        print("-" * 45)
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Urgency: {ticket['urgency']}")
        print(f"Affected users: {ticket['affected_users']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}")

    print("-" * 45)


def show_ticket_details(tickets):
    print("\n--- VIEW TICKET DETAILS ---")

    ticket_id = input("Enter ticket ID (e.g. T001): ").strip().upper()

    try:
        ticket = get_ticket(tickets, ticket_id)

        if ticket is None:
            print("Error: Ticket not found.")
            return

        print("\nTicket details")
        print("-" * 30)

        for key, value in ticket.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def assign_staff(tickets):
    print("\n--- ASSIGN TICKET ---")

    ticket_id = input("Enter ticket ID: ").strip().upper()
    staff_name = input("Enter staff member's name: ").strip()

    try:
        result = assign_ticket(tickets, ticket_id, staff_name)
        print(result)

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def change_ticket_status(tickets):
    print("\n--- UPDATE TICKET STATUS ---")

    ticket_id = input("Enter ticket ID: ").strip().upper()

    print("\nAvailable statuses:")
    print("1. open")
    print("2. in_progress")
    print("3. resolved")

    status_choice = input("Choose the new status: ").strip()

    status_options = {
        "1": "open",
        "2": "in_progress",
        "3": "resolved",
    }

    new_status = status_options.get(status_choice, status_choice.lower())

    try:
        result = update_status(tickets, ticket_id, new_status)
        print(result)

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def show_work_queue(tickets):
    print("\n--- WORK QUEUE ---")

    queue = get_work_queue(tickets)

    if not queue:
        print("There are no unresolved tickets in the work queue.")
        return

    for ticket in queue:
        print("-" * 40)
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}")

    print("-" * 40)


def show_reports(tickets):
    print("\n--- CAMPUSFLOW REPORTS ---")

    report = generate_report(tickets)

    print(f"\nTotal tickets: {report['total_tickets']}")

    print("\nTickets by status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")

    print("\nTickets by priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")


def main():
    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Unable to load saved tickets: {error}")
        print("Please check the saved data before continuing.")
        sys.exit(1)

    print("\nWelcome to CampusFlow Helpdesk!")
    print(f"Loaded {len(tickets)} ticket(s).")

    while True:
        display_menu()

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            create_new_ticket(tickets)

        elif choice == "2":
            show_all_tickets(tickets)

        elif choice == "3":
            show_ticket_details(tickets)

        elif choice == "4":
            assign_staff(tickets)

        elif choice == "5":
            change_ticket_status(tickets)

        elif choice == "6":
            show_work_queue(tickets)

        elif choice == "7":
            show_reports(tickets)

        elif choice == "8":
            try:
                save_tickets(tickets)
                print("Tickets saved successfully.")
            except (OSError, ValueError) as error:
                print(f"Unable to save tickets: {error}")

        elif choice == "9":
            try:
                save_tickets(tickets)
                print("Tickets saved. Goodbye!")
                break
            except (OSError, ValueError) as error:
                print(f"Unable to save tickets: {error}")
                print("Your session is still running. You can try again.")

        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()