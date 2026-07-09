from src.use_cases.repositories.category_repository import CategoryRepository
from entities.category import Category

class CreateCategoryUseCase:

    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo
    
    def execute(self, name: str, budget_limit: float = 0.0) -> Category:
        category = Category(name=name, budget_limit=budget_limit)
        self.account_repo.save(category)
        return category