from pathlib import Path

from src.importer import load_following_data


def main() -> None:
    file_path = Path("data") / "following.json"
    accounts = load_following_data(file_path)

    print(f"Loaded {len(accounts)} accounts.")

    for account in accounts[:5]:
        print(account)


if __name__ == "__main__":
    main()