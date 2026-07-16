# Depot JSON sauvegarde les donnees dans des fichiers .json


import json
import os
from datetime import datetime

from src.entities.account import Account
from src.entities.category import Category
from src.entities.transaction import Transaction, TransactionType
from src.use_cases.interfaces.account_repo import AccountRepo
from src.use_cases.interfaces.category_repo import CategoryRepo

# Dossier ou les fichiers JSON seront sauvegardes
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


# Conversion Transaction 

def _transaction_to_dict(t: Transaction) -> dict:
    return {
        "id": t.id,
        "name": t.name,
        "amount": t.amount,
        "description": t.description,
        "type": t.type.value,
        "created_at": t.created_at.isoformat(),
    }


def _dict_to_transaction(d: dict) -> Transaction:
    return Transaction(
        id=d["id"],
        name=d["name"],
        amount=d["amount"],
        description=d["description"],
        type=TransactionType(d["type"]),
        created_at=datetime.fromisoformat(d["created_at"]),
    )


# Conversion Account 

def _account_to_dict(a: Account) -> dict:
    return {
        "id": a.id,
        "name": a.name,
        "balance": a.balance,
        "transactions": [_transaction_to_dict(t) for t in a.transactions],
    }


def _dict_to_account(d: dict) -> Account:
    transactions = [_dict_to_transaction(t) for t in d.get("transactions", [])]
    return Account(id=d["id"], name=d["name"], balance=d["balance"], transactions=transactions)


# Classes

class JsonAccountRepo(AccountRepo):

    def __init__(self):
        _ensure_data_dir()
        self.filepath = os.path.join(DATA_DIR, "budget.json")

    def _load(self) -> dict:
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_all(self, data: dict) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get(self, account_id: str) -> Account:
        data = self._load()
        if account_id not in data:
            raise ValueError(f"Compte '{account_id}' introuvable.")
        return _dict_to_account(data[account_id])

    def save(self, account: Account) -> None:
        data = self._load()
        data[account.id] = _account_to_dict(account)
        self._save_all(data)

    def get_all(self) -> list:
        return [_dict_to_account(d) for d in self._load().values()]


class JsonCategoryRepo(CategoryRepo):

    def __init__(self):
        _ensure_data_dir()
        self.filepath = os.path.join(DATA_DIR, "categories.json")

    def _load(self) -> dict:
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_all(self, data: dict) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get(self, category_id: str) -> Category:
        data = self._load()
        if category_id not in data:
            raise ValueError(f"Categorie '{category_id}' introuvable.")
        d = data[category_id]
        return Category(id=d["id"], name=d["name"], budget_limit=d["budget_limit"])

    def save(self, category: Category) -> None:
        data = self._load()
        data[category.id] = {"id": category.id, "name": category.name, "budget_limit": category.budget_limit}
        self._save_all(data)

    def get_all(self) -> list:
        return [Category(id=d["id"], name=d["name"], budget_limit=d["budget_limit"]) for d in self._load().values()]
