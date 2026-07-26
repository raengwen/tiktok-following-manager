from pathlib import Path
from datetime import datetime
import json

from src.models import FollowingAccount

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def load_following_data(file_path: Path) -> list[dict]:
    """Load TikTok following data from a JSON export file."""
    
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    try:
        raw_accounts = data["Following"]["Following"]
    except (KeyError, TypeError) as error:
        raise ValueError(
            "The JSON does not match the expected TikTok export structure."
        ) from error

    accounts = []

    for raw_account in raw_accounts:
        try:
            account = FollowingAccount(
                username=raw_account["UserName"],
                date_followed=datetime.strptime(
                    raw_account["Date"],
                    DATE_FORMAT,
                ),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"Invalid following account entry: {raw_account}"
            ) from error

        accounts.append(account)

    return accounts