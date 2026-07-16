

from src.entities.account import Account
from src.use_cases.interfaces.account_repo import AccountRepo


class AccountUseCases:

    def __init__(self, account_repo: AccountRepo):
        self.account_repo = account_repo

    def create_account(self, name: str, balance: float = 0.0) -> Account:
        account = Account(name=name, balance=balance)
        self.account_repo.save(account)
        return account

    def get_all_accounts(self) -> list:
        return self.account_repo.get_all()

    def get_balance(self, account_id: str) -> float:
        return self.account_repo.get(account_id).balance
