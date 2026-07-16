# Le controleur fait le lien entre la CLI et les cas d'usage

from src.use_cases.account_use_cases import AccountUseCases
from src.use_cases.transaction_use_cases import TransactionUseCases
from src.use_cases.category_use_cases import CategoryUseCases


class BudgetController:

    def __init__(
        self,
        accounts: AccountUseCases,
        transactions: TransactionUseCases,
        categories: CategoryUseCases,
    ):
        self._accounts = accounts
        self._transactions = transactions
        self._categories = categories

    # Comptes

    def creer_compte(self, name: str, balance: float = 0.0) -> dict:
        account = self._accounts.create_account(name, balance)
        return {
            "id": account.id,
            "name": account.name,
            "balance": account.balance,
        }

    def lister_comptes(self) -> list:
        accounts = self._accounts.get_all_accounts()
        return [
            {
                "id": a.id,
                "name": a.name,
                "balance": a.balance,
                "nb_transactions": len(a.transactions),
            }
            for a in accounts
        ]

    # Transactions 

    def ajouter_revenu(self, account_id: str, name: str, amount: float, description: str = "") -> dict:
        account = self._transactions.add_income(account_id, name, amount, description)
        return {"account_name": account.name, "new_balance": account.balance, "amount": amount}

    def ajouter_depense(self, account_id: str, name: str, amount: float, description: str = "") -> dict:
        account = self._transactions.add_expense(account_id, name, amount, description)
        return {"account_name": account.name, "new_balance": account.balance, "amount": amount}

    def supprimer_transaction(self, account_id: str, transaction_id: str) -> None:
        self._transactions.delete_transaction(account_id, transaction_id)

    def historique(self, account_id: str) -> list:
        transactions = self._transactions.get_transactions(account_id)
        return [
            {
                "id": t.id,
                "name": t.name,
                "amount": t.amount,
                "type": t.type.value,
                "description": t.description,
                "date": t.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for t in transactions
        ]

    # Categories

    def creer_categorie(self, name: str, budget_limit: float = 0.0) -> dict:
        cat = self._categories.create_category(name, budget_limit)
        return {"id": cat.id, "name": cat.name, "budget_limit": cat.budget_limit}
