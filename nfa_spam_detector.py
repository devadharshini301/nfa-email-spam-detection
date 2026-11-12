"""
Email Spam Detection Using a Nondeterministic Finite Automaton (NFA).

This is an educational, rule-based demonstration. The NFA searches the
combined sender, subject, and body text for configured spam-related words.
It is not a production-grade email filtering system.
"""

from dataclasses import dataclass
import re
from typing import Dict, Set, Tuple


SPAM_KEYWORDS = (
    "free",
    "win",
    "offer",
    "prize",
    "claim",
    "urgent",
    "lottery",
    "cash",
    "click",
    "congratulations",
    "verify",
    "suspended",
)

State = Tuple[str, int]


@dataclass
class NFAResult:
    is_spam: bool
    matched_keywords: list[str]


class EmailSpamNFA:
    """An NFA with one keyword-matching path for each configured keyword."""

    def __init__(self, keywords=SPAM_KEYWORDS):
        self.keywords = tuple(word.lower() for word in keywords)
        self.start_state = "q0"
        self.accept_state = "q_accept"
        self.transitions: Dict[State, Dict[str, Set[State]]] = {}
        self._build_transition_table()

    def _add_transition(self, state: State, character: str, next_state: State):
        self.transitions.setdefault(state, {}).setdefault(character, set()).add(next_state)

    def _build_transition_table(self):
        # q0 represents the search state. It remains active while the input
        # is scanned and can start a new keyword path at every character.
        for keyword in self.keywords:
            for index, character in enumerate(keyword):
                current = (keyword, index)
                if index + 1 == len(keyword):
                    next_state = (self.accept_state, 0)
                else:
                    next_state = (keyword, index + 1)
                self._add_transition(current, character, next_state)

    def scan(self, text: str) -> list[str]:
        """Return every configured keyword found by the NFA."""
        normalized = text.lower()
        active_states: Set[State] = set()
        matched = set()

        for character in normalized:
            next_active: Set[State] = set()

            # NFA nondeterministically starts any keyword whose first
            # character matches the current input character.
            for keyword in self.keywords:
                if keyword[0] == character:
                    if len(keyword) == 1:
                        matched.add(keyword)
                    else:
                        next_active.add((keyword, 1))

            # Advance all currently active keyword paths.
            for keyword, position in active_states:
                if keyword[position] == character:
                    if position + 1 == len(keyword):
                        matched.add(keyword)
                    else:
                        next_active.add((keyword, position + 1))

            # Keep only paths that matched this character. New paths can
            # start at the next input character.
            active_states = next_active

        return sorted(matched)

    def classify(self, sender: str, subject: str, body: str) -> NFAResult:
        email_text = " ".join((sender, subject, body))
        matches = self.scan(email_text)
        return NFAResult(is_spam=bool(matches), matched_keywords=matches)


def main():
    detector = EmailSpamNFA()

    print("=" * 55)
    print("        EMAIL SPAM DETECTION USING NFA")
    print("=" * 55)

    sender = input("Enter sender email: ").strip()
    subject = input("Enter email subject: ").strip()
    body = input("Enter email body: ").strip()

    result = detector.classify(sender, subject, body)

    print("\n--------------- NFA RESULT ---------------")
    if result.is_spam:
        print("Classification : SPAM / SUSPICIOUS")
        print("Matched words  : " + ", ".join(result.matched_keywords))
    else:
        print("Classification : NOT SPAM (no configured keyword found)")
    print("------------------------------------------")
    print("Note: This is a simple academic NFA demonstration.")


if __name__ == "__main__":
    main()
