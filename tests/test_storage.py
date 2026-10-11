import json
import tempfile
import unittest

from pathlib import Path

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class StorageTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "tickets.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_empty_list(self):
        tickets = load_tickets(self.file_path)

        self.assertEqual(tickets, [])

    def test_tickets_survive_save_and_reload(self):
        tickets = []

        create_ticket(
            tickets,
            "Wi-Fi outage",
            "Network",
            "high",
            15,
        )

        save_tickets(tickets, self.file_path)

        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, tickets)

    def test_ticket_id_remains_unique_after_reload(self):
        tickets = []

        create_ticket(
            tickets,
            "First problem",
            "Software",
            "low",
            1,
        )

        save_tickets(tickets, self.file_path)

        loaded_tickets = load_tickets(self.file_path)

        second_ticket = create_ticket(
            loaded_tickets,
            "Second problem",
            "Hardware",
            "low",
            1,
        )

        self.assertEqual(second_ticket["id"], "T002")

    def test_malformed_json_raises_clear_error(self):
        original_content = "{invalid json"

        self.file_path.write_text(
            original_content,
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            load_tickets(self.file_path)

        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            original_content,
        )

    def test_json_object_instead_of_list_is_rejected(self):
        self.file_path.write_text(
            json.dumps({"tickets": []}),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "must be a list"):
            load_tickets(self.file_path)

    def test_duplicate_ids_are_rejected_when_loading(self):
        tickets = []

        first_ticket = create_ticket(
            tickets,
            "First problem",
            "Software",
            "low",
            1,
        )

        duplicate_ticket = first_ticket.copy()

        saved_data = [first_ticket, duplicate_ticket]

        self.file_path.write_text(
            json.dumps(saved_data),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
            load_tickets(self.file_path)


if __name__ == "__main__":
    unittest.main()