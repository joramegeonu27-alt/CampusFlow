import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    get_ticket,
    list_tickets,
)


class TicketTests(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_high_urgency_and_ten_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_high_urgency_with_two_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_with_ten_users_is_high(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_low_urgency_with_four_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_medium_urgency_with_one_user_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_low_urgency_with_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 1)

    def test_zero_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", 0)

    def test_negative_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", -1)

    def test_decimal_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", 1.5)

    def test_boolean_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", True)

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets,
                "   ",
                "Network",
                "low",
                1,
            )

        self.assertEqual(self.tickets, [])

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets,
                "Broken laptop",
                "Food",
                "high",
                2,
            )

    def test_ticket_is_created_correctly(self):
        ticket = create_ticket(
            self.tickets,
            "Campus Wi-Fi is down",
            "network",
            "HIGH",
            15,
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Campus Wi-Fi is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 15)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_ticket_ids_increase(self):
        first = create_ticket(
            self.tickets, "First problem", "Software", "low", 1
        )

        second = create_ticket(
            self.tickets, "Second problem", "Hardware", "low", 1
        )

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_list_tickets_returns_all_tickets(self):
        create_ticket(
            self.tickets, "Wi-Fi problem", "Network", "high", 12
        )

        create_ticket(
            self.tickets, "Broken mouse", "Hardware", "low", 1
        )

        self.assertEqual(len(list_tickets(self.tickets)), 2)

    def test_get_ticket_finds_ticket_by_id(self):
        create_ticket(
            self.tickets, "Wi-Fi problem", "Network", "high", 12
        )

        ticket = get_ticket(self.tickets, "t001")

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket["id"], "T001")


if __name__ == "__main__":
    unittest.main()