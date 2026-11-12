import unittest

from nfa_spam_detector import EmailSpamNFA


class TestEmailSpamNFA(unittest.TestCase):
    def setUp(self):
        self.detector = EmailSpamNFA()

    def test_finds_spam_keywords_case_insensitively(self):
        self.assertEqual(
            self.detector.scan("CONGRATULATIONS! Claim your PRIZE"),
            ["claim", "congratulations", "prize"],
        )

    def test_returns_no_match_for_normal_text(self):
        self.assertEqual(
            self.detector.scan("Meeting notes for tomorrow's project review"),
            [],
        )

    def test_classifies_email_as_spam(self):
        result = self.detector.classify(
            "unknown@example.com",
            "Urgent offer",
            "Click now to claim your free prize",
        )
        self.assertTrue(result.is_spam)
        self.assertIn("urgent", result.matched_keywords)
        self.assertIn("free", result.matched_keywords)

    def test_classifies_email_without_keywords_as_not_spam(self):
        result = self.detector.classify(
            "teacher@example.edu",
            "Project meeting",
            "Please bring your assignment to class tomorrow.",
        )
        self.assertFalse(result.is_spam)
        self.assertEqual(result.matched_keywords, [])


if __name__ == "__main__":
    unittest.main()
