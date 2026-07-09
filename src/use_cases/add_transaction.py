from entities.transaction import Transaction, TransactionType
from src.interface.repositories.account_repository import AccountRepository
from entities.account import Account

class AddTransactionUseCase:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def execute(self, account_id: str, transaction: Transaction) -> Account:
        account = self.account_repo.get_by_id(account_id)
        
        if transaction.type == TransactionType.INCOME:
            account.add_money(transaction)
        else:
            account.remove_money(transaction)

        self.account_repo.save(account)

        return account