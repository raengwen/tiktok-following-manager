import json
from datetime import datetime
from pathlib import Path

from src.models import FollowingAccount
from src.progress import load_progress, save_progress
from src.review import ReviewSession


def make_account(username: str) -> FollowingAccount:
    return FollowingAccount(
        username=username,
        date_followed=datetime(2026, 1, 1),
    )


def test_save_progress_writes_session_state(
    tmp_path: Path,
) -> None:
    accounts = [
        make_account("alice"),
        make_account("bob"),
    ]
    accounts[0].status = "keep"

    session = ReviewSession(
        accounts=accounts,
        current_index=1,
    )

    progress_path = tmp_path / "progress.json"

    save_progress(session, progress_path)

    with progress_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        saved_data = json.load(file)

    assert saved_data["current_index"] == 1
    assert saved_data["accounts"][0]["username"] == "alice"
    assert saved_data["accounts"][0]["status"] == "keep"


def test_load_progress_restores_session_state(
    tmp_path: Path,
) -> None:
    progress_path = tmp_path / "progress.json"

    progress_data = {
        "current_index": 1,
        "accounts": [
            {
                "username": "alice",
                "status": "keep",
                "notes": "Favourite creator",
                "category": "fashion",
            }
        ],
    }

    with progress_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(progress_data, file)

    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    result = load_progress(session, progress_path)

    assert result is True
    assert session.current_index == 1
    assert accounts[0].status == "keep"
    assert accounts[0].notes == "Favourite creator"
    assert accounts[0].category == "fashion"


def test_load_progress_returns_false_when_file_missing(
    tmp_path: Path,
) -> None:
    accounts = [make_account("alice")]
    session = ReviewSession(accounts)

    missing_path = tmp_path / "missing.json"

    result = load_progress(session, missing_path)

    assert result is False
    assert session.current_index == 0
    assert accounts[0].status == "undecided"