# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first time I ran it, the game looked fine. It had a title, a Normal difficulty with a 1 to 100 range, and a debug panel that showed the secret (77). The problems showed up as soon as I played. The hints pointed the wrong way, the score went up after a wrong guess, and the "Attempts left" number started at 7 even though the sidebar said 8 attempts were allowed. After I won, the New Game button didn't really start a new game. It just kept saying "You already won."

Bugs I noticed at the start:

1. **The hints are backwards.** Guessing 90 when the secret was 77 said "Go HIGHER!", and guessing 50 said "Go LOWER!". In `check_guess` the "Too High" result is paired with the "Go HIGHER!" message and "Too Low" with "Go LOWER!".
2. **On every second guess the secret is compared as text.** `app.py` turns the secret into a string when `attempts` is even, so `check_guess` hits the `TypeError` branch and compares strings. "8" > "77" is true for strings, so a guess of 8 counted as "Too High" and gave +5 points.
3. **New Game doesn't reset the game.** The New Game button resets `attempts` and `secret`, but not `status`, `score` or `history`. After a win the status stays "won", so the game is stuck on "You already won." It also always picks the new secret from 1 to 100, whatever the difficulty.
4. **Changing difficulty keeps the old secret.** Switching to Easy (1 to 20) kept the secret at 38, so the game can't be won. The prompt also always says "between 1 and 100".
5. **The attempt counter is off by one.** `attempts` starts at 1 on first load but at 0 after New Game, so the first game gives you 7 guesses on Normal instead of 8. A guess like "abc" also uses up an attempt even though it isn't a number.
6. **The scoring is wrong.** `update_score` adds 5 points for a "Too High" guess on even attempts, and the win formula subtracts one attempt too many.

**Game session log (starter code, before any fixes)**

```
Difficulty: Normal (range 1-100, 8 attempts allowed). Debug panel: Secret 77, Attempts 1
Start        -> "Guess a number between 1 and 100. Attempts left: 7"
Guess 90     -> "📈 Go HIGHER!"            (secret is lower)
Guess 100    -> score back to 0
Guess 8      -> "📈 Go HIGHER!"            score went 0 -> 5 for a wrong guess
Guess 50     -> "📉 Go LOWER!"             (secret is higher), score 5 -> 0
Guess abc    -> "That is not a number."    attempts still went 5 -> 6
Guess 77     -> "🎉 Correct!" "You won! The secret was 77. Final score: 20"
New Game     -> Secret 38, Attempts 0, but "You already won. Start a new game to play again."
                Score still 20, history still shows the old guesses
Difficulty -> Easy (range 1-20): Secret still 38, prompt still says "between 1 and 100", still stuck
```

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 90, secret 77 (Normal) | Hint tells me to go lower | "📈 Go HIGHER!" | none |
| Guess 50, secret 77 (Normal) | Hint tells me to go higher | "📉 Go LOWER!" | none |
| Guess 8 on the 4th attempt, secret 77 | Counted as "Too Low", score does not go up | Counted as "Too High" because "8" > "77" as text, score went 0 -> 5 | none (the `TypeError` is caught inside `check_guess`) |
| Win, then click "New Game 🔁" | Fresh game: score 0, empty history, can guess again | "You already won. Start a new game to play again." on every click, score 20 and old history kept | none |
| Switch difficulty to Easy after a game on Normal | Secret inside 1-20, prompt says 1 to 20 | Secret stays 38, prompt says "between 1 and 100" | none |
| First load on Normal (8 attempts allowed) | "Attempts left: 8" | "Attempts left: 7" | none |
| Guess "abc" | Error message, no attempt used | "That is not a number." and attempts went 5 -> 6 | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
