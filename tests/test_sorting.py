from datetime import datetime

from src.models import FollowingAccount
from src.sorting import sort_accounts


def make_account(
    username: str,
    date_followed: datetime,
    status: str = "undecided",
) -> FollowingAccount:
    """Create an account for use in sorting tests."""

    return FollowingAccount(
        username=username,
        date_followed=date_followed,
        status=status,
    )


def test_sort_accounts_by_username() -> None:
    accounts = [
        make_account("charlie", datetime(2024, 1, 1)),
        make_account("alice", datetime(2023, 1, 1)),
        make_account("bob", datetime(2022, 1, 1)),
    ]

    results = sort_accounts(
        accounts,
        key=lambda account: account.username,
    )

    assert [account.username for account in results] == [
        "alice",
        "bob",
        "charlie",
    ]


def test_sort_accounts_by_date_followed() -> None:
    accounts = [
        make_account("charlie", datetime(2024, 1, 1)),
        make_account("alice", datetime(2023, 1, 1)),
        make_account("bob", datetime(2022, 1, 1)),
    ]

    results = sort_accounts(
        accounts,
        key=lambda account: account.date_followed,
    )

    assert [account.username for account in results] == [
        "bob",
        "alice",
        "charlie",
    ]


def test_sort_accounts_in_reverse_order() -> None:
    accounts = [
        make_account("alice", datetime(2023, 1, 1)),
        make_account("bob", datetime(2022, 1, 1)),
        make_account("charlie", datetime(2024, 1, 1)),
    ]

    results = sort_accounts(
        accounts,
        key=lambda account: account.username,
        reverse=True,
    )

    assert [account.username for account in results] == [
        "charlie",
        "bob",
        "alice",
    ]


def test_sort_accounts_returns_new_list() -> None:
    accounts = [
        make_account("bob", datetime(2022, 1, 1)),
        make_account("alice", datetime(2023, 1, 1)),
    ]

    results = sort_accounts(
        accounts,
        key=lambda account: account.username,
    )

    assert results is not accounts
    assert [account.username for account in accounts] == [
        "bob",
        "alice",
    ]


def test_sort_accounts_preserves_objects() -> None:
    accounts = [
        make_account("bob", datetime(2022, 1, 1)),
        make_account("alice", datetime(2023, 1, 1)),
    ]

    results = sort_accounts(
        accounts,
        key=lambda account: account.username,
    )

    assert results[0] is accounts[1]
    assert results[1] is accounts[0]