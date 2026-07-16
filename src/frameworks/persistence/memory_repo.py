''' Depot en memoire, utilise uniquement pour les tests.
 Les donnees disparaissent quand le programme se ferme'''

from src.use_cases.interfaces.account_repo import AccountRepo
from src.use_cases.interfaces.category_repo import CategoryRepo


class MemoryAccountRepo(AccountRepo):

    def __init__(self):
        self._data = {}

    def get(self, account_id: str):
        if account_id not in self._data:
            raise ValueError(f"Compte '{account_id}' introuvable.")
        return self._data[account_id]

    def save(self, account) -> None:
        self._data[account.id] = account

    def get_all(self) -> list:
        return list(self._data.values())


class MemoryCategoryRepo(CategoryRepo):

    def __init__(self):
        self._data = {}

    def get(self, category_id: str):
        if category_id not in self._data:
            raise ValueError(f"Categorie '{category_id}' introuvable.")
        return self._data[category_id]

    def save(self, category) -> None:
        self._data[category.id] = category

    def get_all(self) -> list:
        return list(self._data.values())
