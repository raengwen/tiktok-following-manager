from datetime import datetime

from src.app import process_choice
from src.models import FollowingAccount
from src.review import ReviewSession


def make_account(username: str) -> FollowingAccount:
    return FollowingAccount(
        username=username,
        date_followed=datetime(2026, 1, 1),
    )


def test_keep_choice_marks_account_as_keep() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    result = process_choice(session, "k")

    assert accounts[0].status == "keep"
    assert result is True


def test_remove_choice_marks_account_as_remove() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    result = process_choice(session, "r")

    assert accounts[0].status == "remove"
    assert result is True


def test_skip_choice_marks_account_as_skipped() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    result = process_choice(session, "s")

    assert accounts[0].status == "skipped"
    assert result is True


def test_quit_choice_returns_false() -> None:
    session = ReviewSession([])

    result = process_choice(session, "q")

    assert result is False


def test_invalid_choice_does_not_advance_session() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    result = process_choice(session, "invalid")

    assert session.current_index == 0
    assert accounts[0].status == "undecided"
    assert result is True