# FIX: Moved the game logic out of app.py into this file (planned with the AI
# assistant, reviewed line by line) so it can be tested with pytest.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX: Always compare numbers. app.py used to turn the secret into text on
    # every second attempt, so "8" > "77" counted as too high. The AI explained
    # the string comparison; I confirmed it with a test for 8 vs 77.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    # FIX: These two hints were swapped. A guess that is too high means go lower.
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def get_hint_message(outcome: str) -> str:
    """Return the hint shown to the player for an outcome from check_guess."""
    # FIX: The hint text used to come back from check_guess as a pair. I kept the
    # starter tests as they were and moved the text here instead of changing the
    # tests to fit the code.
    return HINT_MESSAGES.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1 for the first guess of a game.
    """
    if outcome == "Win":
        # FIX: A win on the first guess is worth 100 points, then 10 less for each
        # extra guess (never below 10). The old formula took off one guess too many.
        points = max(100 - 10 * (attempt_number - 1), 10)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        # FIX: Every wrong guess costs 5 points. "Too High" used to add 5 points
        # on even attempts.
        return current_score - 5

    return current_score
