from pathlib import Path

from src.filters import search_accounts
from src.importer import load_following_data


def main() -> None:
    file_path = Path("data") / "following.json"
    accounts = load_following_data(file_path)

    search_term = input("Search username: ")
    matches = search_accounts(accounts, search_term)

    print(f"\nFound {len(matches)} matching accounts.\n")

    for account in matches[:20]:
        print(
            f"{account.username} — "
            f"followed {account.date_followed:%d %B %Y}"
        )

if __name__ == "__main__":
    main()