from dataclasses import dataclass, field
from datetime import datetime
import uuid
from enum import Enum


class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Transaction:
    name: str
    amount: float
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4))
    created_at: datetime = field(default_factory=datetime.now)
    status: TransactionStatus = TransactionStatus.COMPLETED

