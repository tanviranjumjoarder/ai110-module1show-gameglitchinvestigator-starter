import random
import streamlit as st

# FIX: The game logic now lives in logic_utils.py so pytest can test it.
from logic_utils import (
    check_guess,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def start_new_game(low: int, high: int):
    """Reset everything for a fresh game with a secret in [low, high]."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []


# FIX: Start a fresh game on the first load and whenever the difficulty
# changes, so attempts always start at 0 and the secret is always inside the
# current range. Before, attempts started at 1 and switching to Easy could
# leave a secret like 38 that you could never guess.
if st.session_state.get("difficulty") != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game(low, high)

st.subheader("Make a guess")

# FIX: These two slots are filled in at the end of the script, after the guess
# is handled, so "Attempts left" and the debug info are never one guess behind.
info_slot = st.empty()
debug_slot = st.container()

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: New Game now resets status, score and history too, and uses the
    # range for the current difficulty instead of always 1 to 100. Before, the
    # status stayed "won" and the game was stuck.
    start_new_game(low, high)
    st.success("New game started.")

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
elif submit:
    ok, guess_int, err = parse_guess(raw_guess)

    # FIX: Bad input or a number outside the range shows an error but no longer
    # uses up an attempt.
    if not ok:
        st.error(err)
    elif not low <= guess_int <= high:
        st.error(f"Please guess a number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: Removed the code that turned the secret into a string on even
        # attempts. check_guess now always compares two numbers.
        outcome = check_guess(guess_int, st.session_state.secret)
        message = get_hint_message(outcome)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

# FIX: The prompt uses the real range for the difficulty, not "1 and 100".
info_slot.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with debug_slot:
    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
