"""Tests des entites"""

import pytest
from src.entities.transaction import Transaction, TransactionType
from src.entities.account import Account
from src.entities.category import Category


class TestTransaction:

    def test_creation_valide(self):
        t = Transaction(name="Salaire", amount=1000.0, description="", type=TransactionType.INCOME)
        assert t.name == "Salaire"
        assert t.amount == 1000.0
        assert t.id is not None

    def test_montant_negatif_interdit(self):
        with pytest.raises(ValueError):
            Transaction(name="Test", amount=-50.0, description="", type=TransactionType.INCOME)

    def test_montant_zero_interdit(self):
        with pytest.raises(ValueError):
            Transaction(name="Test", amount=0, description="", type=TransactionType.INCOME)

    def test_nom_vide_interdit(self):
        with pytest.raises(ValueError):
            Transaction(name="", amount=100.0, description="", type=TransactionType.INCOME)


class TestAccount:

    def _income(self, amount):
        return Transaction(name="Test", amount=amount, description="", type=TransactionType.INCOME)

    def _expense(self, amount):
        return Transaction(name="Test", amount=amount, description="", type=TransactionType.EXPENSE)

    def test_creation_valide(self):
        a = Account(name="Mon compte", balance=500.0)
        assert a.balance == 500.0
        assert a.transactions == []

    def test_solde_negatif_interdit(self):
        with pytest.raises(ValueError):
            Account(name="Test", balance=-100.0)

    def test_nom_vide_interdit(self):
        with pytest.raises(ValueError):
            Account(name="", balance=0.0)

    def test_depot_augmente_solde(self):
        a = Account(name="Test", balance=500.0)
        a.deposit(self._income(200.0))
        assert a.balance == 700.0
        assert len(a.transactions) == 1

    def test_retrait_diminue_solde(self):
        a = Account(name="Test", balance=500.0)
        a.withdraw(self._expense(200.0))
        assert a.balance == 300.0

    def test_retrait_solde_insuffisant(self):
        a = Account(name="Test", balance=100.0)
        with pytest.raises(ValueError, match="insuffisant"):
            a.withdraw(self._expense(500.0))

    def test_suppression_revenu_reajuste_solde(self):
        a = Account(name="Test", balance=0.0)
        t = self._income(300.0)
        a.deposit(t)
        a.remove_transaction(t.id)
        assert a.balance == 0.0
        assert len(a.transactions) == 0

    def test_suppression_depense_reajuste_solde(self):
        a = Account(name="Test", balance=500.0)
        t = self._expense(200.0)
        a.withdraw(t)
        a.remove_transaction(t.id)
        assert a.balance == 500.0

    def test_suppression_id_inexistant(self):
        a = Account(name="Test", balance=100.0)
        with pytest.raises(ValueError):
            a.remove_transaction("id-qui-nexiste-pas")


class TestCategory:

    def test_creation_valide(self):
        c = Category(name="Alimentation", budget_limit=300.0)
        assert c.name == "Alimentation"
        assert c.budget_limit == 300.0

    def test_nom_vide_interdit(self):
        with pytest.raises(ValueError):
            Category(name="")

    def test_budget_negatif_interdit(self):
        with pytest.raises(ValueError):
            Category(name="Test", budget_limit=-10.0)
