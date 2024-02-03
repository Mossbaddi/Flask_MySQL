from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class InscriptionForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de Passe', validators=[DataRequired()])
    confirmation = PasswordField('Confirmez le Mot de Passe', validators=[DataRequired(), EqualTo('mot_de_passe')])
    submit = SubmitField('Inscrire')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de Passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')

class AjoutFilmForm(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    realisateur = StringField('Réalisateur')
    annee_sortie = IntegerField('Année de Sortie')
    genre = StringField('Genre')
    submit = SubmitField('Ajouter le Film')

class CritiqueForm(FlaskForm):
    contenu = TextAreaField('Critique', validators=[DataRequired()])
    submit = SubmitField('Publier')

