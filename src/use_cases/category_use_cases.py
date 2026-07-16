

from src.entities.category import Category
from src.use_cases.interfaces.category_repo import CategoryRepo


class CategoryUseCases:
    

    def __init__(self, category_repo: CategoryRepo):
        self.category_repo = category_repo

    def create_category(self, name: str, budget_limit: float = 0.0) -> Category:
        cat = Category(name=name, budget_limit=budget_limit)
        self.category_repo.save(cat)
        return cat

    def get_all_categories(self) -> list:
        return self.category_repo.get_all()
