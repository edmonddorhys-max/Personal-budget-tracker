

from use_cases.repositories.account_repository import AccountRepository

class DeleteTransactionUseCase:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def execute(self, account_id: str, transaction_id: str) -> None:
       account = self.account_repo.get_by_id(account_id)
       
       account.remove_transaction(transaction_id)
       
       self.account_repo.save(account)
       