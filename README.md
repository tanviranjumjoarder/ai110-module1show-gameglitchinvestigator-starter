# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Purpose.** This is a number guessing game built with Streamlit. The game picks a secret number in a range that depends on the difficulty (Easy 1-20, Normal 1-100, Hard 1-50). You guess, the game says whether to go higher or lower, and you win if you find the number before you run out of attempts. You score more points for winning in fewer guesses and lose 5 points for each wrong guess.

**Bugs I found** (full details and a reproduction table are in `reflection.md`):

1. The hints were backwards: "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!".
2. On every second guess the secret was turned into a string, so numbers were compared as text ("8" > "77"), which gave the wrong result.
3. New Game didn't reset the status, score or history, so after a win or a loss the game was stuck. It also always picked the secret from 1 to 100.
4. Changing the difficulty kept the old secret, so on Easy the secret could be 38 with a 1 to 20 range. The prompt always said "between 1 and 100".
5. The attempt counter started at 1 on the first game, so Normal only gave 7 guesses. Typing something that isn't a number also used up an attempt.
6. Scoring was wrong: a "Too High" guess added 5 points on even attempts, and the win formula took off one guess too many.

**Fixes I applied:**

- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` from `app.py` into `logic_utils.py`, and `app.py` imports them.
- `check_guess` always compares numbers and returns only `"Win"`, `"Too High"` or `"Too Low"`, which is what the starter tests expect. The hint text moved to a new `get_hint_message` helper, with the two hints swapped back the right way.
- `update_score` takes 5 points off for any wrong guess. A win is worth 100 on the first guess and 10 less for each extra guess, never below 10.
- `app.py` has a `start_new_game` function that resets everything. It runs on the first load, when you click New Game, and when you change difficulty.
- Bad input and numbers outside the range show an error without using an attempt.
- The prompt shows the real range, and "Attempts left" and the debug panel update right after each guess.
- Added 6 new pytest tests and a `pytest.ini` so that plain `pytest` can import `logic_utils`.

## 📸 Demo Walkthrough

A game I played on the fixed version (the secret is visible in the "Developer Debug Info" panel):

1. The game opens on Normal: "Guess a number between 1 and 100. Attempts left: 8". The secret is 72.
2. I guess 90. The game shows "📉 Go LOWER!", Attempts left drops to 7 and the score goes to -5.
3. I guess 8. The game shows "📈 Go HIGHER!" (before the fix this guess counted as too high). Attempts left is 6 and the score is -10.
4. I type "abc". The game shows "That is not a number." and Attempts left stays at 6.
5. I guess 150. The game shows "Please guess a number between 1 and 100." and Attempts left stays at 6.
6. I guess 72. The game shows "🎉 Correct!" and "You won! The secret was 72. Final score: 70" (-10 plus 80 for winning on the 3rd guess).
7. I click "New Game 🔁". The game shows "New game started.", Attempts left is back to 8, the score is 0 and the history is empty.
8. I switch the difficulty to Easy. The prompt changes to "Guess a number between 1 and 20. Attempts left: 6" and the new secret (19) is inside that range.
9. On Hard (1 to 50, 5 attempts, secret 3) I guess 10 five times. Each guess says "📉 Go LOWER!", and after the fifth the game shows "Out of attempts! The secret was 3. Score: -25". Submitting again shows "Game over. Start a new game to try again.", and New Game starts a fresh game.

## 🧪 Test Results

```
$ pytest -v
configfile: pytest.ini
testpaths: tests
collecting ... collected 9 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 11%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 22%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 33%]
tests/test_game_logic.py::test_small_guess_is_too_low_not_compared_as_text PASSED [ 44%]
tests/test_game_logic.py::test_hints_point_the_right_way PASSED          [ 55%]
tests/test_game_logic.py::test_wrong_guess_never_adds_points PASSED      [ 66%]
tests/test_game_logic.py::test_win_points_depend_on_attempts PASSED      [ 77%]
tests/test_game_logic.py::test_range_for_each_difficulty PASSED          [ 88%]
tests/test_game_logic.py::test_parse_guess PASSED                        [100%]

============================== 9 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] Not attempted for this submission.
