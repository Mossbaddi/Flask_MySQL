import time
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exc
import pymysql
import subprocess

db = SQLAlchemy()

def wait_for_db(host, port, user, password, db):
    retries = 5
    while retries:
        try:
            conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db)
            print("Connexion à la base de données réussie.")
            conn.close()
            return True
        except pymysql.MySQLError as e:
            print("En attente de la base de données...")
            print(e)
            retries -= 1
            time.sleep(5)

    print("Échec de la connexion à la base de données après plusieurs tentatives.")
    return False

import os

def initialize_migrations():
    """Initialise les migrations si le dossier n'existe pas."""
    try:
        subprocess.run(["flask", "db", "init"], check=True)
        print("Initialisation des migrations réussie.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'initialisation des migrations : {e}")

def migrate_and_upgrade():
    """Vérifie l'existence du dossier de migrations, l'initialise si nécessaire, puis applique les migrations."""
    migrations_path = '/app/migrations'  # Ajustez selon la structure de votre projet
    if not os.path.exists(migrations_path):
        print("Le dossier 'migrations' n'existe pas. Initialisation en cours...")
        initialize_migrations()

    try:
        # Exécuter la commande Flask pour générer une nouvelle migration
        subprocess.run(["flask", "db", "migrate"], check=True)
        # Exécuter la commande Flask pour appliquer les migrations
        subprocess.run(["flask", "db", "upgrade"], check=True)
        print("Migrations appliquées avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution des migrations : {e}")

if __name__ == "__main__":
    # Exemple d'utilisation de variables d'environnement (à remplacer par vos valeurs)
    db_host = "db"  # Nom du service Docker pour MySQL dans docker-compose.yml   
    db_port = 3306
    db_user = "root"
    db_password = "exemple"
    db_name = "critiques_de_films"

    if wait_for_db(db_host, db_port, db_user, db_password, db_name):
        print("Migrations Flask...")
        migrate_and_upgrade()
    else:
        print("Impossible de démarrer l'application Flask en raison d'un problème de base de données.")