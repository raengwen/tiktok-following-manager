from datetime import datetime

from src.filters import search_accounts
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
