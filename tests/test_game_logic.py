from logic_utils import (
    check_guess,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Tests for the bugs I fixed ---

def test_small_guess_is_too_low_not_compared_as_text():
    # Bug: on even attempts the secret became "77", and "8" > "77" as text.
    # 8 is smaller than 77, so it must be "Too Low".
    assert check_guess(8, 77) == "Too Low"
    assert check_guess(8, "77") == "Too Low"
    assert check_guess(100, 50) == "Too High"


def test_hints_point_the_right_way():
    # Bug: "Too High" used to say "Go HIGHER!" and "Too Low" said "Go LOWER!".
    assert "LOWER" in get_hint_message("Too High")
    assert "HIGHER" in get_hint_message("Too Low")
    assert "Correct" in get_hint_message("Win")


def test_wrong_guess_never_adds_points():
    # Bug: a "Too High" guess on an even attempt added 5 points.
    for attempt in range(1, 9):
        assert update_score(0, "Too High", attempt) == -5
        assert update_score(0, "Too Low", attempt) == -5


def test_win_points_depend_on_attempts():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 3) == 80
    assert update_score(0, "Win", 20) == 10  # never below 10


def test_range_for_each_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_parse_guess():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess(" 7 ") == (True, 7, None)
    assert parse_guess("abc") == (False, None, "That is not a number.")
    assert parse_guess("") == (False, None, "Enter a guess.")
