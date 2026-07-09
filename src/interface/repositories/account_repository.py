from abc import ABC, abstractmethod
from entities.account import Account

class AccountRepository(ABC):
    @abstractmethod
    def get_by_id(self, account_id: str) -> Account:
        ...

    @abstractmethod
    def save(self, account: Account) -> None:
        ...