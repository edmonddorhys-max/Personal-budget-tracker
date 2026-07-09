from entities.account import Account
from src.interface.repositories.account_repository import AccountRepository

class InMemoryAccountRepository(AccountRepository):
    def __init__(self):
        self._accounts: dict[str, Account] = {}

    def get_by_id(self, account_id: str ) -> Account:
        if account_id not in self._accounts:
            raise ValueError(f"Account {account_id} not found")
        return self._accounts[account_id]
    
    def save(self, account: Account) -> None:
        self._accounts[account.id] = account