from dataclasses import dataclass, field
import uuid


@dataclass
class Category:
    name: str
    budget_limit: float = 0.0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Le nom ne peut pas etre vide.")
        if self.budget_limit < 0:
            raise ValueError("Le budget ne peut pas etre negatif.")