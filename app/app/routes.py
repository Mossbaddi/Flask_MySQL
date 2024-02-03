from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import InscriptionForm, LoginForm
from .models import Utilisateur
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.mot_de_passe.data)
        new_user = Utilisateur(nom=form.nom.data, email=form.email.data, mot_de_passe_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('inscription.html', form=form)

@main.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = LoginForm()
    # Logique pour la vérification des identifiants
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.mot_de_passe_hash, form.mot_de_passe.data):
            # Logique pour établir la session de l'utilisateur
            return redirect(url_for('main.index'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('connexion.html', form=form)
