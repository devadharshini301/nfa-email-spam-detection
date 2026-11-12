# Email Spam Detection Using NFA

A beginner-friendly Python project that demonstrates how a **Nondeterministic Finite Automaton (NFA)** can identify suspicious email text by searching for a set of configured spam-related keywords.

## Project objective

To demonstrate the application of Finite Automata in a simple email spam detection task. The program checks the sender, subject, and body for configured words such as `free`, `win`, `offer`, `prize`, `claim`, and `urgent`.

## Technologies

- Python 3.9+
- NFA state-transition simulation
- Python standard library (no external packages required)

## Project files

| File | Purpose |
|---|---|
| `nfa_spam_detector.py` | NFA implementation and command-line program |
| `test_nfa_spam_detector.py` | Unit tests |
| `requirements.txt` | Dependency information |

## How the NFA works

The NFA has a search state called **q0** and a separate matching path for each configured keyword.

1. The program combines the sender, subject, and body into one input string.
2. The input is converted to lowercase.
3. At each character, q0 can start matching any keyword that begins with that character.
4. Multiple keyword paths can be active at the same time. This is the nondeterministic behaviour.
5. If a path matches every character of a keyword, that keyword is recorded as accepted.
6. If at least one configured keyword is found, the email is labelled **SPAM / SUSPICIOUS**. Otherwise, it is labelled **NOT SPAM**.

### Simplified state diagram

Each keyword has its own path. For example, the path for the keyword `win` is:

```text
                 w          i          n
q0 (search) -------> (win,1) -----> (win,2) -----> q_accept
   |                    |              |
   +-- can start other keyword paths at every input character
```

The full NFA runs all keyword paths in parallel. The program represents active states as a set.

## Run the project

### 1. Install Python

Install Python 3.9 or later from https://www.python.org/downloads/.

### 2. Clone this repository

```bash
git clone https://github.com/devadharshini301/nfa-email-spam-detection.git
cd nfa-email-spam-detection
```

### 3. Run the program

```bash
python nfa_spam_detector.py
```

Enter the sender email, subject, and body when prompted.

### 4. Run the tests

```bash
python -m unittest -v
```

## Example

**Input**

- Sender: `offers@example.com`
- Subject: `Congratulations! You have a prize`
- Body: `Click now to claim your free gift.`

**Expected result**

```text
Classification : SPAM / SUSPICIOUS
Matched words  : claim, congratulations, free, prize
```

## Important limitation

This is an academic automata-theory demonstration, not a real-world spam filter. A legitimate email may contain one of these words, and spam may avoid them. Real spam detection normally combines multiple signals such as sender reputation, links, message features, and machine-learning models.

## Author

Created as an academic project to demonstrate NFA-based text pattern recognition.
