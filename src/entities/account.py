from dataclasses import dataclass, field
from src.entities.transaction import Transaction, TransactionType
import uuid


@dataclass
class Account:
    name: str
    balance: float = 0.0
    transactions: list = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if self.balance < 0:
            raise ValueError("Le solde ne peut pas etre negatif.")
        if not self.name.strip():
            raise ValueError("Le nom ne peut pas etre vide.")

    def deposit(self, transaction: Transaction):
        """Ajoute un revenu au compte."""
        self.balance += transaction.amount
        self.transactions.append(transaction)

    def withdraw(self, transaction: Transaction):
        """Retire une depense du compte."""
        if transaction.amount > self.balance:
            raise ValueError("Solde insuffisant.")
        self.balance -= transaction.amount
        self.transactions.append(transaction)

    def remove_transaction(self, transaction_id: str):
        """Supprime une transaction et reajuste le solde."""
        for t in self.transactions:
            if t.id == transaction_id:
                # Inverser l'effet : si c'etait un revenu on soustrait, sinon on ajoute
                if t.type == TransactionType.INCOME:
                    self.balance -= t.amount
                else:
                    self.balance += t.amount
                self.transactions.remove(t)
                return
        raise ValueError("Transaction introuvable.")