from datetime import datetime

import pytest

from src.models import FollowingAccount
from src.review import ReviewSession


def make_account(username: str) -> FollowingAccount:
    return FollowingAccount(
        username=username,
        date_followed=datetime(2026, 1, 1),
    )


def test_session_starts_at_first_account() -> None:
    accounts = [
        make_account("alice"),
        make_account("bob"),
    ]

    session = ReviewSession(accounts)

    assert session.current_index == 0
    assert session.current_account is accounts[0]
    assert session.progress == (0, 2)
    assert session.is_complete is False


def test_review_current_updates_status_and_advances() -> None:
    accounts = [
        make_account("alice"),
        make_account("bob"),
    ]

    session = ReviewSession(accounts)

    session.review_current("keep")

    assert accounts[0].status == "keep"
    assert session.current_index == 1
    assert session.current_account is accounts[1]


def test_review_current_records_previous_status() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    session.review_current("remove")

    assert session.history == [(0, "undecided")]


def test_session_is_complete_after_last_account() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    session.review_current("keep")

    assert session.is_complete is True
    assert session.current_account is None
    assert session.progress == (1, 1)


def test_review_raises_error_when_complete() -> None:
    session = ReviewSession([])

    with pytest.raises(
        IndexError,
        match="There are no accounts left to review.",
    ):
        session.review_current("keep")

def test_undo_restores_previous_status() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    session.review_current("keep")
    session.undo_last_review()

    assert accounts[0].status == "undecided"


def test_undo_moves_back_to_previous_account() -> None:
    accounts = [
        make_account("alice"),
        make_account("bob"),
    ]
    session = ReviewSession(accounts)

    session.review_current("keep")
    session.undo_last_review()

    assert session.current_index == 0
    assert session.current_account is accounts[0]


def test_undo_removes_action_from_history() -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    session.review_current("keep")
    session.undo_last_review()

    assert session.history == []


def test_undo_raises_error_when_history_is_empty() -> None:
    session = ReviewSession([])

    with pytest.raises(
        IndexError,
        match="There are no review actions to undo.",
    ):
        session.undo_last_review()