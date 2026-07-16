"""Tests des cas d'usage"""

import pytest
from src.frameworks.persistence.memory_repo import MemoryAccountRepo, MemoryCategoryRepo
from src.use_cases.budget_service import BudgetService


@pytest.fixture
def service():
    """Cree un service avec des depots en memoire (rapide, pas de fichiers)."""
    return BudgetService(
        account_repo=MemoryAccountRepo(),
        category_repo=MemoryCategoryRepo(),
    )


@pytest.fixture
def service_avec_compte(service):
    """Cree un service avec un compte de 1000$ deja existant."""
    account = service.create_account("Compte Test", balance=1000.0)
    return service, account


class TestCreateAccount:

    def test_creation_simple(self, service):
        account = service.create_account("Mon compte", 500.0)
        assert account.name == "Mon compte"
        assert account.balance == 500.0

    def test_solde_par_defaut_zero(self, service):
        account = service.create_account("Vide")
        assert account.balance == 0.0

    def test_nom_vide_interdit(self, service):
        with pytest.raises(ValueError):
            service.create_account("")


class TestAddIncome:

    def test_revenu_augmente_le_solde(self, service_avec_compte):
        service, account = service_avec_compte
        updated = service.add_income(account.id, "Salaire", 500.0)
        assert updated.balance == 1500.0

    def test_montant_negatif_interdit(self, service_avec_compte):
        service, account = service_avec_compte
        with pytest.raises(ValueError):
            service.add_income(account.id, "Test", -100.0)


class TestAddExpense:

    def test_depense_diminue_le_solde(self, service_avec_compte):
        service, account = service_avec_compte
        updated = service.add_expense(account.id, "Loyer", 300.0)
        assert updated.balance == 700.0

    def test_solde_insuffisant_interdit(self, service_avec_compte):
        service, account = service_avec_compte
        with pytest.raises(ValueError, match="insuffisant"):
            service.add_expense(account.id, "Achat", 5000.0)


class TestDeleteTransaction:

    def test_supprimer_revenu_reajuste_solde(self, service_avec_compte):
        service, account = service_avec_compte
        updated = service.add_income(account.id, "Salaire", 400.0)
        assert updated.balance == 1400.0

        transaction_id = updated.transactions[-1].id
        service.delete_transaction(account.id, transaction_id)
        assert service.get_balance(account.id) == 1000.0


class TestGetTransactions:

    def test_transactions_du_plus_recent_au_plus_ancien(self, service_avec_compte):
        service, account = service_avec_compte
        service.add_income(account.id, "Premier", 100.0)
        service.add_expense(account.id, "Deuxieme", 50.0)
        service.add_income(account.id, "Troisieme", 200.0)

        transactions = service.get_transactions(account.id)
        assert len(transactions) == 3
        dates = [t.created_at for t in transactions]
        assert dates == sorted(dates, reverse=True)


class TestGetAllAccounts:

    def test_retourne_liste_vide(self, service):
        assert service.get_all_accounts() == []

    def test_retourne_tous_les_comptes(self, service):
        service.create_account("A")
        service.create_account("B")
        assert len(service.get_all_accounts()) == 2


class TestCreateCategory:

    def test_creation_simple(self, service):
        cat = service.create_category("Alimentation", 400.0)
        assert cat.name == "Alimentation"
        assert cat.budget_limit == 400.0

    def test_nom_vide_interdit(self, service):
        with pytest.raises(ValueError):
            service.create_category("")
