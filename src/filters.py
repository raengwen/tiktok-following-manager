from src.models import FollowingAccount


def search_accounts(
    accounts: list[FollowingAccount],
    search_term: str,
) -> list[FollowingAccount]:
    """Return accounts whose usernames contain the search term."""

    normalised_term = search_term.strip().lower()

    if not normalised_term:
        return accounts.copy()

    return [
        account
        for account in accounts
        if normalised_term in account.username.lower()
    ]