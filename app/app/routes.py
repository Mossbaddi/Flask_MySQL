from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import InscriptionForm, LoginForm, AjoutFilmForm, CritiqueForm
from .models import Utilisateur, Film, Critique, LikeFilm, LikeCritique
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


@main.route('/ajouter-film', methods=['GET', 'POST'])
def ajouter_film():
    form = AjoutFilmForm()
    if form.validate_on_submit():
        film = Film(titre=form.titre.data, realisateur=form.realisateur.data, annee_sortie=form.annee_sortie.data, genre=form.genre.data)
        db.session.add(film)
        db.session.commit()
        flash('Film ajouté avec succès !')
        return redirect(url_for('main.index'))
    return render_template('ajouter_film.html', form=form)

@main.route('/films')
def films():
    films = Film.query.all()
    return render_template('films.html', films=films)

@main.route('/films/<int:id>')
def film_detail(id):
    film = Film.query.get_or_404(id)
    return render_template('film_detail.html', film=film)

@main.route('/films/<int:id>/critique', methods=['GET', 'POST'])
def ajouter_critique(id):
    form = CritiqueForm()
    film = Film.query.get_or_404(id)
    if form.validate_on_submit():
        critique = Critique(contenu=form.contenu.data, film=film)
        db.session.add(critique)
        db.session.commit()
        return redirect(url_for('main.film_detail', id=id))
    return render_template('ajouter_critique.html', form=form, film=film)

@main.route('/like-film/<int:id_film>')
def like_film(id_film):
    film = Film.query.get_or_404(id_film)
    like_existant = LikeFilm.query.filter_by(id_utilisateur=session['user_id'], id_film=id_film).first()
    if not like_existant:
        nouveau_like = LikeFilm(id_utilisateur=session['user_id'], id_film=id_film)
        db.session.add(nouveau_like)
        db.session.commit()
    return redirect(url_for('main.film_detail', id=id_film))

@main.route('/like-critique/<int:id_critique>')
def like_critique(id_critique):
    critique = Critique.query.get_or_404(id_critique)
    like_existant = LikeCritique.query.filter_by(id_utilisateur=session['user_id'], id_critique=id_critique).first()
    if not like_existant:
        nouveau_like = LikeCritique(id_utilisateur=session['user_id'], id_critique=id_critique)
        db.session.add(nouveau_like)
        db.session.commit()
    return redirect(url_for('main.film_detail', id=critique.id_film))
