
from entities.account import Account
from src.use_cases.interface.repositories import AccountRepository


class CreateAccountUseCase:
    def __init__(self,account_repo: AccountRepository):
        self.account_repo = account_repo

    def execute(self, name: str) -> Account:
        account = Account(name=name)
        self.account_repo.save(account)
        return account

