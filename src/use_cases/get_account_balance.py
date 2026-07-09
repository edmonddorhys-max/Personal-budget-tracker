from src.interface.repositories.account_repository import AccountRepository
from entities.account import Account

class GetAccountBalance:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def execute(self, id: str )-> float:
        account = self.account_repo.get_by_id(id)
        return account.balance
