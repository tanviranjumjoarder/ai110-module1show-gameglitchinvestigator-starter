**Name:** Tanvir Anjum Joarder  
**Z Number:** Z23981706  
**Course:** AI110 Foundations of AI Engineering, Fall 2026 (CodePath @ FAU)

# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The game looked normal when I first opened it. It had a title, Normal difficulty with a range of 1 to 100, and a debug panel that showed the secret number. Once I started guessing it fell apart. The hints were backwards, my score went up after a wrong guess, and after I won, New Game didn't start a new game. It just kept saying "You already won."

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 90, secret is 77 | Tells me to go lower | "Go HIGHER!" | none |
| Guess 8 on my 4th try, secret is 77 | Too low, I lose points | Counted as too high and my score went up by 5 | none |
| Win, then click New Game | A new game starts | "You already won." every time, old score and history still there | none |
| Switch to Easy (1 to 20) | New secret between 1 and 20 | Secret stayed at 38, prompt still said 1 to 100 | none |
| Type "abc" | Error, no attempt used | Error shown, but it still used an attempt | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code. I asked it why a guess of 8 counted as too high when the secret was 77, and it said the app turned the secret into text on every second guess, and as text "8" comes after "77". That matched my log because it only happened on even tries, and my test for 8 vs 77 passed after the fix.

One suggestion I didn't take: the starter tests expect check_guess to return just "Win", but the code returned a pair with the message too. The AI offered to change the tests so they unpack the pair. I didn't want to change the tests to fit broken code, so I made check_guess return only the result and moved the message into a small helper. The three starter tests pass without any changes.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I called a bug fixed when a test using the input from my bug log passed and the same input worked in the real game. One test checks that a wrong guess loses 5 points on every attempt from 1 to 8, since the old bug only showed up on even attempts. Running the tests also showed a setup problem: plain `pytest` couldn't find logic_utils, so I added a pytest.ini. The AI helped me turn my bug log into tests, and I checked that each one would have failed on the old code. The New Game and difficulty bugs are in app.py, so I tested those by playing the game.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button, Streamlit runs the whole script again from the top. Normal variables get reset each time, so the game would forget the secret. Session state is like a dictionary that stays between reruns, so the secret, score and attempts are kept there. The order of the script matters too. The old code showed "Attempts left" before it handled the guess, so the number was always one behind.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I want to keep writing a bug log before fixing anything and turning each row into a test. It made it easy to tell when something was really fixed. Next time I'll ask the AI to explain a bug before I ask for a fix, and I'll work on one bug at a time. This project made me trust AI code a lot less just because it runs. This game ran fine and still had six bugs.
