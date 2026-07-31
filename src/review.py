from dataclasses import dataclass, field

from src.models import FollowingAccount


@dataclass
class ReviewSession:
    accounts: list[FollowingAccount]
    current_index: int = 0
    history: list[tuple[int, str]] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        """Return True when every account has been reviewed."""
        return self.current_index >= len(self.accounts)

    @property
    def current_account(self) -> FollowingAccount | None:
        """Return the current account, or None when the session is complete."""
        if self.is_complete:
            return None

        return self.accounts[self.current_index]

    @property
    def progress(self) -> tuple[int, int]:
        """Return the current position and total number of accounts."""
        return self.current_index, len(self.accounts)

    def review_current(self, status: str) -> None:
        """Set the current account's status and move to the next account."""
        account = self.current_account

        if account is None:
            raise IndexError("There are no accounts left to review.")

        self.history.append((self.current_index, account.status))
        account.status = status
        self.current_index += 1

    def undo_last_review(self) -> None:
        """Restore the account changed by the most recent review."""

        if not self.history:
            raise IndexError("There are no review actions to undo.")

        account_index, previous_status = self.history.pop()

        self.accounts[account_index].status = previous_status
        self.current_index = account_index