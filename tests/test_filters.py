from datetime import datetime

from src.filters import search_accounts
from src.filters import filter_by_status
from src.models import FollowingAccount


def make_account(username: str) -> FollowingAccount:
    return FollowingAccount(
        username=username,
        date_followed=datetime(2026, 1, 1),
    )


def test_search_accounts_matches_partial_username() -> None:
    accounts = [
        make_account("girlswhotravel"),
        make_account("booklover"),
    ]

    results = search_accounts(accounts, "travel")

    assert results == [accounts[0]]


def test_search_accounts_is_case_insensitive() -> None:
    accounts = [make_account("GirlsWhoTravel")]

    results = search_accounts(accounts, "TRAVEL")

    assert results == accounts


def test_empty_search_returns_all_accounts_in_new_list() -> None:
    accounts = [
        make_account("alice"),
        make_account("bob"),
    ]

    results = search_accounts(accounts, "   ")

    assert results == accounts
    assert results is not accounts

def test_filter_by_status_returns_matching_accounts() -> None:
    accounts = [
        FollowingAccount(
            username="alice",
            date_followed=datetime(2026, 1, 1),
            status="keep",
        ),
        FollowingAccount(
            username="bob",
            date_followed=datetime(2026, 1, 1),
            status="remove",
        ),
        FollowingAccount(
            username="charlie",
            date_followed=datetime(2026, 1, 1),
            status="keep",
        ),
    ]

    results = filter_by_status(accounts, "keep")

    assert [account.username for account in results] == [
        "alice",
        "charlie",
    ]


def test_filter_by_status_is_case_insensitive() -> None:
    accounts = [
        FollowingAccount(
            username="alice",
            date_followed=datetime(2026, 1, 1),
            status="keep",
        ),
    ]

    results = filter_by_status(accounts, "KEEP")

    assert results == accounts


def test_filter_by_status_returns_empty_list_for_no_matches() -> None:
    accounts = [
        FollowingAccount(
            username="alice",
            date_followed=datetime(2026, 1, 1),
            status="undecided",
        ),
    ]

    results = filter_by_status(accounts, "remove")

    assert results == []