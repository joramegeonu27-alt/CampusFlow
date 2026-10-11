import unittest

from campusflow.reports import generate_report
from campusflow.tickets import create_ticket


class ReportTests(unittest.TestCase):

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)

        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

    def test_report_counts_tickets_correctly(self):
        tickets = []

        create_ticket(
            tickets,
            "Wi-Fi outage",
            "Network",
            "high",
            15,
        )

        create_ticket(
            tickets,
            "Broken mouse",
            "Hardware",
            "low",
            1,
        )

        tickets[0]["status"] = "in_progress"
        tickets[1]["status"] = "resolved"

        report = generate_report(tickets)

        self.assertEqual(report["total_tickets"], 2)

        self.assertEqual(
            report["by_status"]["in_progress"],
            1,
        )

        self.assertEqual(
            report["by_status"]["resolved"],
            1,
        )

        self.assertEqual(
            report["by_priority"]["critical"],
            1,
        )

        self.assertEqual(
            report["by_priority"]["low"],
            1,
        )


if __name__ == "__main__":
    unittest.main()