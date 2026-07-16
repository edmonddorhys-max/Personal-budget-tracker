# Le controleur fait le lien entre la CLI et les cas d'usage
# La CLI ne connait pas BudgetService directement, elle passe par ici

from src.use_cases.budget_service import BudgetService


class BudgetController:

    def __init__(self, service: BudgetService):
        self.service = service

    #Comptes

    def creer_compte(self, name: str, balance: float = 0.0) -> dict:
        account = self.service.create_account(name, balance)
        return {
            "id": account.id,
            "name": account.name,
            "balance": account.balance,
        }

    def lister_comptes(self) -> list:
        accounts = self.service.get_all_accounts()
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
        account = self.service.add_income(account_id, name, amount, description)
        return {"account_name": account.name, "new_balance": account.balance, "amount": amount}

    def ajouter_depense(self, account_id: str, name: str, amount: float, description: str = "") -> dict:
        account = self.service.add_expense(account_id, name, amount, description)
        return {"account_name": account.name, "new_balance": account.balance, "amount": amount}

    def supprimer_transaction(self, account_id: str, transaction_id: str) -> None:
        self.service.delete_transaction(account_id, transaction_id)

    def historique(self, account_id: str) -> list:
        transactions = self.service.get_transactions(account_id)
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
        cat = self.service.create_category(name, budget_limit)
        return {"id": cat.id, "name": cat.name, "budget_limit": cat.budget_limit}
