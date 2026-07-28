from collections.abc import Callable

from src.models import FollowingAccount


def sort_accounts(
    accounts: list[FollowingAccount],
    key: Callable[[FollowingAccount], object],
    reverse: bool = False,
) -> list[FollowingAccount]:
    """Return a sorted copy of the accounts."""
    return sorted(
        accounts,
        key=key,
        reverse=reverse
    )