

from src.entities.transaction import Transaction, TransactionType
from src.use_cases.interfaces.account_repo import AccountRepo


class TransactionUseCases:


    def __init__(self, account_repo: AccountRepo):
        self.account_repo = account_repo

    def add_income(self, account_id: str, name: str, amount: float, description: str = ""):
        account = self.account_repo.get(account_id)
        t = Transaction(name=name, amount=amount, description=description, type=TransactionType.INCOME)
        account.deposit(t)
        self.account_repo.save(account)
        return account

    def add_expense(self, account_id: str, name: str, amount: float, description: str = ""):
        account = self.account_repo.get(account_id)
        t = Transaction(name=name, amount=amount, description=description, type=TransactionType.EXPENSE)
        account.withdraw(t)
        self.account_repo.save(account)
        return account

    def delete_transaction(self, account_id: str, transaction_id: str) -> None:
        account = self.account_repo.get(account_id)
        account.remove_transaction(transaction_id)
        self.account_repo.save(account)

    def get_transactions(self, account_id: str) -> list:
        account = self.account_repo.get(account_id)
        return sorted(account.transactions, key=lambda t: t.created_at, reverse=True)
