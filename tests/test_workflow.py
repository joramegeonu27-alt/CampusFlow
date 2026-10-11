import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    change_status,
    find_ticket,
    get_work_queue,
    reopen_ticket,
)


class WorkflowTests(unittest.TestCase):

    def setUp(self):
        self.tickets = []

        create_ticket(
            self.tickets,
            "Wi-Fi outage",
            "Network",
            "high",
            15,
        )

        create_ticket(
            self.tickets,
            "Broken mouse",
            "Hardware",
            "low",
            1,
        )

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            find_ticket(self.tickets, "T999")

    def test_blank_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", " ")

    def test_ticket_can_be_assigned(self):
        ticket = assign_ticket(
            self.tickets,
            "T001",
            "Ada Lovelace",
        )

        self.assertEqual(ticket["assigned_to"], "Ada Lovelace")

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

        self.assertEqual(self.tickets[0]["status"], "open")

    def test_assigned_ticket_can_be_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")

        change_status(self.tickets, "T001", "in_progress")

        self.assertEqual(
            self.tickets[0]["status"],
            "in_progress",
        )

        change_status(self.tickets, "T001", "resolved")

        self.assertEqual(
            self.tickets[0]["status"],
            "resolved",
        )

    def test_ticket_cannot_skip_workflow(self):
        assign_ticket(self.tickets, "T001", "Ada")

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "resolved")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "closed")

    def test_resolved_ticket_cannot_be_assigned_again(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Grace")

    def test_resolved_ticket_can_be_reopened(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        ticket = reopen_ticket(self.tickets, "T001")

        self.assertEqual(ticket["status"], "open")

    def test_unresolved_queue_is_sorted_by_priority(self):
        create_ticket(
            self.tickets,
            "Another Wi-Fi issue",
            "Network",
            "high",
            10,
        )

        create_ticket(
            self.tickets,
            "Software issue",
            "Software",
            "low",
            4,
        )

        queue = get_work_queue(self.tickets)

        queue_ids = [ticket["id"] for ticket in queue]

        self.assertEqual(
            queue_ids,
            ["T001", "T003", "T004", "T002"],
        )

    def test_resolved_tickets_are_excluded_from_queue(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        queue = get_work_queue(self.tickets)

        queue_ids = [ticket["id"] for ticket in queue]

        self.assertNotIn("T001", queue_ids)


if __name__ == "__main__":
    unittest.main()