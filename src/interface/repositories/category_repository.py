from abc import ABC, abstractmethod
from entities.category import Category

class CategoryRepository(ABC):
   
    @abstractmethod
    def get_by_id(self, category_id: str) -> Category:
        ...

    @abstractmethod
    def save(self, category: Category) -> None:
        ...