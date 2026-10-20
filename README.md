**Name:** Tanvir Anjum Joarder  
**Z Number:** Z23981706  
**Course:** AI110 Foundations of AI Engineering, Fall 2026 (CodePath @ FAU)

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

This is a number guessing game made with Streamlit. The game picks a secret number and you try to guess it before you run out of attempts. After each guess it tells you to go higher or lower. Easy is 1 to 20, Normal is 1 to 100 and Hard is 1 to 50.

Bugs I found (the full log is in `reflection.md`):

- The hints were backwards.
- On every second guess the secret was compared as text, so 8 counted as higher than 77.
- New Game didn't reset the score, history or status, so the game got stuck after a win.
- Changing difficulty kept the old secret, even when it was outside the new range.
- Attempts started at 1 instead of 0, and typing something that isn't a number used up a try.
- Scoring was off. Some wrong guesses added points instead of taking them away.

What I fixed: I moved the game logic from `app.py` into `logic_utils.py` so I could test it. `check_guess` now always compares numbers and returns just "Win", "Too High" or "Too Low", and the hint text is in its own function with the hints the right way round. A wrong guess always costs 5 points. In `app.py`, New Game and changing difficulty both start a fresh game now, and bad input shows an error without using a try. I also added 6 tests and a `pytest.ini` so plain `pytest` works.

## 📸 Demo Walkthrough

1. Run `python -m streamlit run app.py`. The game starts on Normal and says "Guess a number between 1 and 100. Attempts left: 8".
2. Open "Developer Debug Info" to see the secret, then guess a number above it. The game says "📉 Go LOWER!" and you lose 5 points.
3. Guess a small number like 8 when the secret is bigger. It says "📈 Go HIGHER!" now. Before the fix this counted as too high.
4. Type "abc". You get "That is not a number." and Attempts left stays the same.
5. Guess the secret. You get "🎉 Correct!" and your final score.
6. Click "New Game 🔁". Attempts go back to 8, the score goes to 0 and the history is cleared.
7. Switch to Easy. The prompt changes to 1 to 20 and the new secret is in that range.

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

- [ ] I didn't do any stretch features.
