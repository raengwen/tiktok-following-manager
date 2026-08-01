import json
from pathlib import Path

from src.models import FollowingAccount
from src.review import ReviewSession


def save_progress(
    session: ReviewSession,
    file_path: Path,
) -> None:
    """Save the current review-session state to a JSON file."""

    progress_data = {
        "current_index": session.current_index,
        "accounts": [
            {
                "username": account.username,
                "status": account.status,
                "notes": account.notes,
                "category": account.category,
            }
            for account in session.accounts
        ],
    }

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            progress_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

def load_progress(
    session: ReviewSession,
    file_path: Path,
) -> bool:
    """
    Apply saved progress to a review session.

    Return True when progress was loaded.
    Return False when no progress file exists.
    """

    if not file_path.exists():
        return False

    with file_path.open("r", encoding="utf-8") as file:
        progress_data = json.load(file)

    saved_accounts = {
        saved_account["username"]: saved_account
        for saved_account in progress_data["accounts"]
    }

    for account in session.accounts:
        saved_account = saved_accounts.get(account.username)

        if saved_account is None:
            continue

        account.status = saved_account.get(
            "status",
            "undecided",
        )
        account.notes = saved_account.get("notes", "")
        account.category = saved_account.get("category")

    saved_index = progress_data.get("current_index", 0)

    session.current_index = min(
        saved_index,
        len(session.accounts),
    )

    return True