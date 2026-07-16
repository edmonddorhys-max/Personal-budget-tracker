''' 
Interface CLI,  menu interactif '''

import sys

# Correction encodage Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src.interface_adapters.controller import BudgetController


def sep():
    print("-" * 50)


def ask(label: str) -> str:
    return input(f"  > {label}: ").strip()


def ask_float(label: str, allow_zero: bool = True) -> float:
    """Demande un nombre a l'utilisateur.
    Si allow_zero=False, boucle jusqu'a avoir un montant positif.
    """
    while True:
        raw = ask(label)
        if not raw and allow_zero:
            return 0.0
        try:
            value = float(raw)
            if not allow_zero and value <= 0:
                print("  [!] Le montant doit etre superieur a 0.")
                continue
            return value
        except ValueError:
            print("  [!] Entrez un nombre valide (ex: 150.50)")


def ok(msg: str):
    print(f"\n  [OK] {msg}\n")


def err(msg: str):
    print(f"\n  [ERREUR] {msg}\n")


# Menus

def menu_creer_compte(ctrl: BudgetController):
    print("\n  -- Creer un compte --")
    name = ask("Nom du compte")
    if not name:
        err("Le nom ne peut pas etre vide.")
        return
    balance = ask_float("Solde initial (0 par defaut, Entree pour ignorer)")
    try:
        result = ctrl.creer_compte(name, balance)
        ok(f"Compte '{result['name']}' cree ! Solde: {result['balance']:.2f}$")
        print(f"  ID: {result['id']}")
    except ValueError as e:
        err(str(e))


def menu_lister_comptes(ctrl: BudgetController):
    print("\n  -- Mes comptes --")
    accounts = ctrl.lister_comptes()
    if not accounts:
        print("  Aucun compte. Creez-en un d'abord.")
        return
    sep()
    for i, a in enumerate(accounts, 1):
        print(f"  {i}. {a['name']:<25} {a['balance']:>10.2f}$  ({a['nb_transactions']} transactions)")
        print(f"     ID: {a['id']}")
    sep()


def _choisir_compte(ctrl: BudgetController):
    """Affiche la liste et retourne l'id du compte choisi."""
    accounts = ctrl.lister_comptes()
    if not accounts:
        print("  Aucun compte disponible. Creez-en un d'abord.")
        return None
    print("\n  Comptes disponibles:")
    for i, a in enumerate(accounts, 1):
        print(f"    {i}. {a['name']} (solde: {a['balance']:.2f}$)")
    choice = ask("Numero du compte")
    try:
        return accounts[int(choice) - 1]["id"]
    except (ValueError, IndexError):
        err("Choix invalide.")
        return None


def menu_ajouter_revenu(ctrl: BudgetController):
    print("\n  -- Ajouter un revenu --")
    account_id = _choisir_compte(ctrl)
    if not account_id:
        return
    name = ask("Nom (ex: Salaire)")
    amount = ask_float("Montant ($)", allow_zero=False)
    desc = ask("Description (optionnel)")
    try:
        result = ctrl.ajouter_revenu(account_id, name, amount, desc)
        ok(f"Revenu de {result['amount']:.2f}$ ajoute ! Nouveau solde: {result['new_balance']:.2f}$")
    except ValueError as e:
        err(str(e))


def menu_ajouter_depense(ctrl: BudgetController):
    print("\n  -- Ajouter une depense --")
    account_id = _choisir_compte(ctrl)
    if not account_id:
        return
    name = ask("Nom (ex: Loyer)")
    amount = ask_float("Montant ($)", allow_zero=False)
    desc = ask("Description (optionnel)")
    try:
        result = ctrl.ajouter_depense(account_id, name, amount, desc)
        ok(f"Depense de {result['amount']:.2f}$ enregistree ! Nouveau solde: {result['new_balance']:.2f}$")
    except ValueError as e:
        err(str(e))


def menu_historique(ctrl: BudgetController):
    print("\n  -- Historique des transactions --")
    account_id = _choisir_compte(ctrl)
    if not account_id:
        return
    try:
        transactions = ctrl.historique(account_id)
        if not transactions:
            print("  Aucune transaction sur ce compte.")
            return
        sep()
        for t in transactions:
            signe = "+" if t["type"] == "income" else "-"
            print(f"  {t['date']}  {signe}{t['amount']:.2f}$  {t['name']}")
            if t["description"]:
                print(f"    -> {t['description']}")
            print(f"    ID: {t['id']}")
        sep()
    except ValueError as e:
        err(str(e))


def menu_supprimer_transaction(ctrl: BudgetController):
    print("\n  -- Supprimer une transaction --")
    account_id = _choisir_compte(ctrl)
    if not account_id:
        return
    try:
        transactions = ctrl.historique(account_id)
        if not transactions:
            print("  Aucune transaction sur ce compte.")
            return
        print("\n  Transactions:")
        for i, t in enumerate(transactions, 1):
            signe = "+" if t["type"] == "income" else "-"
            print(f"    {i}. [{t['date']}] {signe}{t['amount']:.2f}$ - {t['name']}")
        choice = ask("Numero a supprimer")
        transaction_id = transactions[int(choice) - 1]["id"]
        confirm = ask("Confirmer ? (oui/non)").lower()
        if confirm in ("oui", "o"):
            ctrl.supprimer_transaction(account_id, transaction_id)
            ok("Transaction supprimee.")
        else:
            print("  Annule.")
    except (ValueError, IndexError) as e:
        err(str(e))


def menu_creer_categorie(ctrl: BudgetController):
    print("\n  -- Creer une categorie --")
    name = ask("Nom (ex: Alimentation)")
    if not name:
        err("Le nom ne peut pas etre vide.")
        return
    limit = ask_float("Plafond budget$ (0 = pas de limite)")
    try:
        result = ctrl.creer_categorie(name, limit)
        ok(f"Categorie '{result['name']}' creee !")
    except ValueError as e:
        err(str(e))


# Boucle principale

def run(ctrl: BudgetController):
    print("\n  Bienvenue dans votre Budget Tracker!")

    while True:
        print()
        print("=" * 50)
        print("       PERSONAL BUDGET TRACKER")
        print("=" * 50)
        print("  1. Creer un compte")
        print("  2. Lister mes comptes")
        print("  3. Ajouter un revenu")
        print("  4. Ajouter une depense")
        print("  5. Voir l'historique")
        print("  6. Supprimer une transaction")
        print("  7. Creer une categorie")
        print("  0. Quitter")
        print("-" * 50)

        choice = ask("Votre choix")

        if choice == "0":
            print("\n  Au revoir!\n")
            break
        elif choice == "1":
            menu_creer_compte(ctrl)
        elif choice == "2":
            menu_lister_comptes(ctrl)
        elif choice == "3":
            menu_ajouter_revenu(ctrl)
        elif choice == "4":
            menu_ajouter_depense(ctrl)
        elif choice == "5":
            menu_historique(ctrl)
        elif choice == "6":
            menu_supprimer_transaction(ctrl)
        elif choice == "7":
            menu_creer_categorie(ctrl)
        else:
            print("  [!] Option invalide. Entrez un chiffre entre 0 et 7.")

        input("\n  Appuyez sur Entree pour continuer...")
