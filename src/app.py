from pathlib import Path

from src.filters import search_accounts
from src.importer import load_following_data
from src.review import ReviewSession
from src.progress import save_progress,load_progress

def main() -> None:
    """Load account data and start the review application."""
    file_path = Path("data/following.json")
    progress_path = Path("data/review_progress.json")

    accounts = load_following_data(file_path)
    session = ReviewSession(accounts)

    progress_loaded = load_progress(
        session,
        progress_path,
    )

    print(f"Loaded {len(accounts)} accounts.")

    if progress_loaded:
        print(
            "Previous progress restored. "
            f"Resuming at account {session.current_index + 1}."
        )
    else:
        print("No previous progress found. Starting a new review.")

    run_review_session(
        session,
        progress_path,
    )


def display_account(session: ReviewSession) -> None:
    """Display the current account and review progress."""
    account = session.current_account

    if account is None:
        return

    current_number = session.current_index + 1
    total_accounts = len(session.accounts)

    print()
    print("=" * 40)
    print(f"Account {current_number} of {total_accounts}")
    print(f"Username: {account.username}")
    print(f"Followed: {account.date_followed:%d %B %Y}")
    print(f"Status: {account.status}")
    print("=" * 40)


def display_menu() -> None:
    """Display the available review actions."""
    print("[K] Keep")
    print("[R] Remove")
    print("[S] Skip")
    print("[U] Undo")
    print("[Q] Quit")

def get_user_choice() -> str:
    """Read and normalise the user's menu choice."""
    return input("Choice: ").strip().lower()

def process_choice(
    session: ReviewSession,
    choice: str,
) -> bool:
    """
    Process one menu choice.

    Return False when the application should quit.
    Return True when it should continue.
    """
    if choice == "k":
        session.review_current("keep")
    elif choice == "r":
        session.review_current("remove")
    elif choice == "s":
        session.review_current("skipped")
    elif choice == "u":
        try:
            session.undo_last_review()
        except IndexError as error:
            print(error)
    elif choice == "q":
        return False
    else:
        print("Invalid choice. Please enter K, R, S, U or Q.")

    return True

def run_review_session(
    session: ReviewSession,
    progress_path: Path,
) -> None:
    while not session.is_complete:
        display_account(session)
        display_menu()

        choice = get_user_choice()
        should_continue = process_choice(session, choice)

        if not should_continue:
            save_progress(session, progress_path)
            print("Progress saved.")
            print("Review session ended.")
            return

    save_progress(session, progress_path)
    print("All accounts have been reviewed.")
    print("Progress saved.")

if __name__ == "__main__":
    main()