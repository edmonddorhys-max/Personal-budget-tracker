'''Toute la logique metier du budget tracker
 Ce fichier ne sait pas comment les donnees sont sauvegardees
 (JSON, SQL, memoire...)il utilise juste les interfaces '''

from src.entities.account import Account
from src.entities.category import Category
from src.entities.transaction import Transaction, TransactionType
from src.use_cases.interfaces.account_repo import AccountRepo
from src.use_cases.interfaces.category_repo import CategoryRepo


class BudgetService:
    """Contient tous les cas d'usage de l'application."""

    def __init__(self, account_repo: AccountRepo, category_repo: CategoryRepo):
        self.account_repo = account_repo
        self.category_repo = category_repo

    # Comptes 

    def create_account(self, name: str, balance: float = 0.0) -> Account:
        account = Account(name=name, balance=balance)
        self.account_repo.save(account)
        return account

    def get_all_accounts(self) -> list:
        return self.account_repo.get_all()

    def get_balance(self, account_id: str) -> float:
        return self.account_repo.get(account_id).balance

    # Transactions

    def add_income(self, account_id: str, name: str, amount: float, description: str = "") -> Account:
        account = self.account_repo.get(account_id)
        t = Transaction(name=name, amount=amount, description=description, type=TransactionType.INCOME)
        account.deposit(t)
        self.account_repo.save(account)
        return account

    def add_expense(self, account_id: str, name: str, amount: float, description: str = "") -> Account:
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

    # Categories

    def create_category(self, name: str, budget_limit: float = 0.0) -> Category:
        cat = Category(name=name, budget_limit=budget_limit)
        self.category_repo.save(cat)
        return cat

    def get_all_categories(self) -> list:
        return self.category_repo.get_all()
