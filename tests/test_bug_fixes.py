import sys
from unittest.mock import MagicMock

# Configure the streamlit mock so module-level app code doesn't crash on import.
# - selectbox must return a real difficulty string (used as a dict key)
# - button must return False so submit/new_game blocks don't execute
# - session_state.__contains__ returns True so initialization blocks are skipped
# - session_state.status = "playing" so the early-exit block is skipped
st_mock = MagicMock()
st_mock.sidebar.selectbox.return_value = "Normal"
st_mock.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
st_mock.button.return_value = False
st_mock.checkbox.return_value = False
session_state = MagicMock()
session_state.__contains__ = MagicMock(return_value=True)
session_state.status = "playing"
st_mock.session_state = session_state
sys.modules["streamlit"] = st_mock

from app import check_guess, get_range_for_difficulty


# --- Bug: check_guess messages were swapped ---
# When guess > secret the original code returned "Go HIGHER!" (should be "Go LOWER!")
# When guess < secret the original code returned "Go LOWER!" (should be "Go HIGHER!")

def test_too_high_message_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"

def test_too_high_message_does_not_say_go_higher():
    _, message = check_guess(60, 50)
    assert "HIGHER" not in message, f"Message incorrectly says HIGHER when guess is too high: {message}"

def test_too_low_message_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message}"

def test_too_low_message_does_not_say_go_lower():
    _, message = check_guess(40, 50)
    assert "LOWER" not in message, f"Message incorrectly says LOWER when guess is too low: {message}"

def test_correct_guess_returns_win():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


# --- Bug: on even attempts secret was cast to str, breaking numeric comparison ---
# check_guess now always receives integer inputs; verify it handles them correctly

def test_check_guess_integer_inputs_too_high():
    # Would previously fail on even attempts due to str cast causing wrong string comparison
    outcome, message = check_guess(99, 10)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_check_guess_integer_inputs_too_low():
    outcome, message = check_guess(1, 99)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# --- Bug: Hard difficulty range was 1-50, easier than Normal's 1-100 ---

def test_hard_range_is_harder_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high, (
        f"Hard upper bound ({hard_high}) should exceed Normal's ({normal_high})"
    )

def test_hard_range_values():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 500


# --- Bug: new_game button and hint message used hardcoded range instead of difficulty range ---
# Verify get_range_for_difficulty returns correct bounds for every difficulty

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_all_ranges_have_positive_lower_bound():
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, _ = get_range_for_difficulty(difficulty)
        assert low >= 1, f"{difficulty} lower bound should be >= 1, got {low}"

def test_all_ranges_high_greater_than_low():
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, high = get_range_for_difficulty(difficulty)
        assert high > low, f"{difficulty} high ({high}) must be greater than low ({low})"
