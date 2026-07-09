from dataclasses import dataclass, field
from entities.transaction import Transaction
import uuid


@dataclass
class Account:
    name: str
    balance: float = 0.0
    transactions: list[Transaction] = field(default_factory=list)
    id: str = field(default_factory= lambda: str(uuid.uuid4()))
   
    def __post_init__(self):
        if self.balance <0:
            raise ValueError("An account cannot be created with a negative balance.")
        if not self.name or self.name.strip() == "":
            raise ValueError("Your name cannot be empty")

    def add_money(self, transaction: Transaction)->None:
        if transaction.amount <= 0:
            raise ValueError("An account cannot be created with a negative balance.")
        self.balance += transaction.amount
        self.transactions.append(transaction)
        

    def remove_money(self, transaction: Transaction)-> None:
        if transaction.amount <= 0:
            raise ValueError("The amount must be positive.")
        if self.balance < transaction.amount:
            raise ValueError("Insufficient balance")
        self.balance -= transaction.amount
        self.transactions.append(transaction)

    def remove_transaction(self, transaction_id: str) -> None:
       for transaction in self.transactions:
            if transaction.id == transaction_id:
               
                self.balance -= transaction.amount
                
                self.transactions.remove(transaction)
                
                break