"""
Genere ou complete un CSV simulant un export caisse/ERP boulangerie-patisserie
(chaine fictive "Craquelin", pour projet portfolio uniquement).

Usage:
    python3 generate_sales_csv.py init --rows 6000
    python3 generate_sales_csv.py append --rows 50

Mode init   : cree le fichier avec un historique de depart (6 mois).
Mode append : ajoute N nouvelles ventes a la suite du fichier existant,
              datees autour d'aujourd'hui, comme un vrai export quotidien.
"""

import argparse
import csv
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

CSV_PATH = Path("data/raw/export_caisse_craquelin.csv")
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

DIM_BOUTIQUES_PATH  = Path("data/raw/dim_boutiques.csv")
DIM_BOUTIQUES_PATH .parent.mkdir(parents=True, exist_ok=True)

BOUTIQUES = [
    {"id": "PAR11-2015", "nom": "Craquelin Paris Bastille", "ville": "Paris", "code_postal": "75011", "date_ouverture": "2015-03-15"},
    {"id": "PAR18-2016", "nom": "Craquelin Paris Montmartre", "ville": "Paris", "code_postal": "75018", "date_ouverture": "2016-09-01"},
    {"id": "PAR04-2016", "nom": "Craquelin Paris Marais", "ville": "Paris", "code_postal": "75004", "date_ouverture": "2016-11-20"},
    {"id": "PAR06-2017", "nom": "Craquelin Paris Saint-Germain", "ville": "Paris", "code_postal": "75006", "date_ouverture": "2017-05-10"},
    {"id": "PAR17-2018", "nom": "Craquelin Paris Batignolles", "ville": "Paris", "code_postal": "75017", "date_ouverture": "2018-02-28"},
    {"id": "PAR12-2019", "nom": "Craquelin Paris Nation", "ville": "Paris", "code_postal": "75012", "date_ouverture": "2019-06-15"},
    {"id": "PAR14-2020", "nom": "Craquelin Paris Montparnasse", "ville": "Paris", "code_postal": "75014", "date_ouverture": "2020-01-20"},
    {"id": "PAR20-2021", "nom": "Craquelin Paris Belleville", "ville": "Paris", "code_postal": "75020", "date_ouverture": "2021-09-05"},
    {"id": "BOU92-2020", "nom": "Craquelin Boulogne-Billancourt", "ville": "Boulogne-Billancourt", "code_postal": "92100", "date_ouverture": "2020-10-12"},
    {"id": "SDE93-2022", "nom": "Craquelin Saint-Denis", "ville": "Saint-Denis", "code_postal": "93200", "date_ouverture": "2022-03-08"},
]

PRODUITS = [
    ("BAG001", "Baguette Tradition", "Boulangerie", 1.30),
    ("BAG002", "Baguette Classique", "Boulangerie", 1.05),
    ("PAI010", "Pain de Campagne", "Boulangerie", 3.20),
    ("PAI011", "Pain aux Cereales", "Boulangerie", 3.50),
    ("VIE001", "Croissant", "Viennoiserie", 1.20),
    ("VIE002", "Pain au Chocolat", "Viennoiserie", 1.30),
    ("VIE003", "Chausson aux Pommes", "Viennoiserie", 2.10),
    ("VIE004", "Pain aux Raisins", "Viennoiserie", 1.40),
    ("PAT001", "Eclair Chocolat", "Patisserie", 3.90),
    ("PAT002", "Tarte Citron", "Patisserie", 4.20),
    ("PAT003", "Paris-Brest", "Patisserie", 4.50),
    ("PAT004", "Millefeuille", "Patisserie", 4.30),
    ("SAN001", "Sandwich Jambon Beurre", "Snacking", 5.50),
    ("SAN002", "Sandwich Poulet Crudites", "Snacking", 6.20),
    ("SAN003", "Sandwich Thon", "Snacking", 5.90),
    ("SAL001", "Salade Cesar", "Snacking", 7.50),
    ("BOI001", "Bouteille Eau 50cl", "Boisson", 1.50),
    ("BOI002", "Coca-Cola 33cl", "Boisson", 2.20),
    ("BOI003", "Jus Orange 25cl", "Boisson", 2.50),
    ("CAF001", "Cafe Expresso", "Boisson chaude", 1.80),
]

PAIEMENTS = ["CB", "Especes", "Especes", "CB", "CB", "Ticket Restaurant", "cb", "ESPECES", "Cheque"]

COMMENTAIRES_OK = ["", "", "", "", "RAS", "Client fidele", "Commande groupe", "Retrait sur place"]
COMMENTAIRES_MOJIBAKE = [
    "Ã  emporter", "commande pour l'Ã©quipe", "erreur de caisse rÃ©initialisÃ©e",
    "rÃ©clamation client", "problÃ¨me de rendu monnaie",
]

DATE_FORMATS = [
    lambda d: d.strftime("%Y-%m-%d"),
    lambda d: d.strftime("%d/%m/%Y"),
    lambda d: d.strftime("%d-%m-%Y"),
    lambda d: d.strftime("%Y-%m-%dT%H:%M:%S"),
    lambda d: d.strftime("%d/%m/%Y %H:%M"),
]

HEADER = ["id_transaction", "date_vente", "boutique_id", "code_produit", "nom_produit",
          "categorie", "quantite", "prix_unitaire_ttc", "moyen_paiement", "id_client", "commentaire"]


def build_row(tx_id: int, dt: datetime) -> list[str]:
    date_str = random.choice(DATE_FORMATS)(dt)
    boutique = random.choice(BOUTIQUES)
    point_vente = boutique["id"]
    code_prod, nom_prod, categorie, prix_base = random.choice(PRODUITS)

    r = random.random()
    if r < 0.03:
        quantite = ""
    elif r < 0.05:
        quantite = str(-random.randint(1, 2))
    elif r < 0.06:
        quantite = "trois"
    else:
        quantite = str(random.randint(1, 5))

    r2 = random.random()
    prix_val = round(prix_base * random.uniform(0.95, 1.0), 2)
    if r2 < 0.03:
        prix_str = ""
    elif r2 < 0.25:
        prix_str = str(prix_val).replace(".", ",")
    elif r2 < 0.28:
        prix_str = f"{prix_val}\u20ac"
    else:
        prix_str = str(prix_val)

    moyen_paiement = random.choice(PAIEMENTS)
    id_client = "" if random.random() < 0.7 else f"CL{random.randint(1000, 9999)}"

    if random.random() < 0.04:
        commentaire = random.choice(COMMENTAIRES_MOJIBAKE)
    else:
        commentaire = random.choice(COMMENTAIRES_OK)

    return [f"TX{tx_id:06d}", date_str, point_vente, code_prod, nom_prod, categorie,
            quantite, prix_str, moyen_paiement, id_client, commentaire]


def maybe_malformed_line(tx_id: int, dt: datetime) -> str | None:
    """Retourne parfois une ligne brute mal formee, sinon None."""
    if random.random() > 0.05:
        return None
    kind = random.choice(["missing_cols", "extra_col", "wrong_sep"])
    date_str = dt.strftime("%d/%m/%Y")
    if kind == "missing_cols":
        return f"TX{tx_id:06d},{date_str},PAR11-2015,BAG001,Baguette Tradition,Boulangerie,2\n"
    if kind == "extra_col":
        return f"TX{tx_id:06d},{date_str},PAR17-2018,PAT002,Tarte Citron,Patisserie,1,4.20,CB,,RAS,EXTRA\n"
    return f"TX{tx_id:06d};{date_str};PAR12-2019;VIE001;Croissant;Viennoiserie;3;1.20;CB;;\n"


def last_tx_id(path: Path) -> int:
    """Cherche le plus grand id_transaction deja present dans le fichier."""
    if not path.exists():
        return 0
    max_id = 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            for m in re.finditer(r"TX(\d{6})", line):
                max_id = max(max_id, int(m.group(1)))
    return max_id


def cmd_init(args):
    n_rows = args.rows
    start_date = datetime.now() - timedelta(days=180)

    rows = []
    for i in range(1, n_rows + 1):
        day_offset = random.randint(0, 180)
        hour = random.randint(6, 20)
        minute = random.randint(0, 59)
        dt = start_date + timedelta(days=day_offset, hours=hour, minutes=minute)
        rows.append(build_row(i, dt))

    n_dupes = int(n_rows * 0.015)
    for _ in range(n_dupes):
        rows.append(random.choice(rows[:n_rows]).copy())
    random.shuffle(rows)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)

    with open(CSV_PATH, "a", encoding="utf-8") as f:
        for tx_id in range(n_rows + 1, n_rows + 4):
            dt = start_date + timedelta(days=random.randint(0, 180))
            line = maybe_malformed_line(tx_id, dt)
            if line is None:
                line = maybe_malformed_line(tx_id, dt) or ""
            f.write(line or "")

    print(f"[init] {n_rows} ventes generees dans {CSV_PATH} (+ doublons + lignes sales)")


def cmd_append(args):
    n_rows = args.rows
    start_id = last_tx_id(CSV_PATH) + 1
    now = datetime.now()

    lines_to_add = []
    for offset, tx_id in enumerate(range(start_id, start_id + n_rows)):
        # les nouvelles ventes sont datees dans les dernieres 24h, comme un export du jour
        dt = now - timedelta(minutes=random.randint(0, 60 * 24))
        malformed = maybe_malformed_line(tx_id, dt)
        if malformed:
            lines_to_add.append(malformed)
        else:
            row = build_row(tx_id, dt)
            lines_to_add.append(",".join(f'"{v}"' if "," in v else v for v in row) + "\n")

    with open(CSV_PATH, "a", encoding="utf-8") as f:
        f.writelines(lines_to_add)

    print(f"[append] {n_rows} nouvelles ventes ajoutees (id {start_id} a {start_id + n_rows - 1})")


def cmd_dim_boutiques(args):
    with open(DIM_BOUTIQUES_PATH , "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nom", "ville", "code_postal", "date_ouverture"])  # liste des noms de colonnes
        writer.writeheader()          # écrit l'en-tête automatiquement à partir de fieldnames
        writer.writerows(BOUTIQUES)   # écrit directement les dicts, un par ligne


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generateur de ventes caisse Craquelin (fictif)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Cree le fichier avec un historique de depart")
    p_init.add_argument("--rows", type=int, default=6000)
    p_init.set_defaults(func=cmd_init)

    p_append = sub.add_parser("append", help="Ajoute de nouvelles ventes au fichier existant")
    p_append.add_argument("--rows", type=int, default=50)
    p_append.set_defaults(func=cmd_append)

    p_boutiques = sub.add_parser("boutiques", help="Cree le fichier avec la dimension boutiques")
    p_boutiques.set_defaults(func=cmd_dim_boutiques)

    args = parser.parse_args()
    args.func(args)
