from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class TransactionType(Enum):
    INCOME = "income"    # Revenu
    EXPENSE = "expense"  # Depense


@dataclass
class Transaction:
    name: str
    amount: float
    description: str
    type: TransactionType
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Le montant doit etre positif.")
        if not self.name.strip():
            raise ValueError("Le nom ne peut pas etre vide.")