import sys
import os

# Ajoute la racine du projet au chemin Python
# Cela permet d'utiliser "from src.xxx import yyy" partout
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- Composition Root ---
# Le seul endroit ou on cree les objets et on branche les couches ensemble.

from src.frameworks.persistence.json_repo import JsonAccountRepo, JsonCategoryRepo
from src.use_cases.account_use_cases import AccountUseCases
from src.use_cases.transaction_use_cases import TransactionUseCases
from src.use_cases.category_use_cases import CategoryUseCases
from src.interface_adapters.controller import BudgetController
from src.frameworks.cli.cli import run


if __name__ == "__main__":
    # 1. Couche frameworks : les depots concrets (JSON)
    account_repo = JsonAccountRepo()
    category_repo = JsonCategoryRepo()

    # 2. Couche use_cases : les cas d'usage
    accounts = AccountUseCases(account_repo)
    transactions = TransactionUseCases(account_repo)
    categories = CategoryUseCases(category_repo)

    # 3. Couche interface_adapters : le controleur
    controller = BudgetController(accounts, transactions, categories)

    # 4. Couche frameworks : lancer la CLI
    run(controller)
