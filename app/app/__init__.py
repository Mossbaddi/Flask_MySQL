from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuration de la base de données et autres configurations
    app.config['SECRET_KEY'] = 'votre_clé_secrète'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:exemple@db/critiques_de_films'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    # Creation de la base de données
    with app.app_context():
        db.create_all()

    # Migrations
    migrate.init_app(app, db)

    # Importation et enregistrement des blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
