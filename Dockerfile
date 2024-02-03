# Utiliser une image Python officielle
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances et installer les packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copier le reste du code source de l'application
COPY app/ ./app

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=app/app

# Exposer le port sur lequel l'application s'exécutera
EXPOSE 5000

# Copier le script d'entrée
COPY ./app/manage_db.py /usr/src/app/manage_db.py
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# Lancer le script d'entrée
ENTRYPOINT ["/bin/bash","/usr/src/app/entrypoint.sh"]

# Commande pour exécuter l'application Flask
# CMD ["flask", "run", "--host=0.0.0.0"]

# ENTRYPOINT [ "tail" , "-f" , "/dev/null" ]