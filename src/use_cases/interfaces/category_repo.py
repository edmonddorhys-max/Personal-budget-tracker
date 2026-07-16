# Contrat (interface) que tout depot de categories doit respecter

from abc import ABC, abstractmethod


class CategoryRepo(ABC):

    @abstractmethod
    def get(self, category_id: str):
        """Retourne une categorie par son id. Leve ValueError si introuvable."""
        pass

    @abstractmethod
    def save(self, category) -> None:
        """Sauvegarde une categorie."""
        pass

    @abstractmethod
    def get_all(self) -> list:
        """Retourne toutes les categories."""
        pass
