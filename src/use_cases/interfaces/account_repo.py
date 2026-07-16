''' Contrat (interface) que tout depot de comptes doit respecter
 La couche use_cases ne sait PAS si les donnees sont en JSON, SQL, memoire...
 Elle sait juste que ces 3 methodes existent'''

from abc import ABC, abstractmethod


class AccountRepo(ABC):

    @abstractmethod
    def get(self, account_id: str):
        """Retourne un compte par son id. Leve ValueError si introuvable."""
        ...

    @abstractmethod
    def save(self, account) -> None:
        """Sauvegarde un compte (creation ou mise a jour)."""
        ...

    @abstractmethod
    def get_all(self) -> list:
        """Retourne tous les comptes."""
        ...
