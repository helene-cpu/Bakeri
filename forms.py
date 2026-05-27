from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    navn = StringField("Navn", validators=[InputRequired()])
    brukernavn = StringField("Brukernavn", validators=[InputRequired()])
    passord = PasswordField("Passord", validators=[InputRequired()])
    submit = SubmitField("Registrer")

class LoginForm(FlaskForm):
    brukernavn = StringField("Brukernavn", validators=[InputRequired()])
    passord = PasswordField("Passord", validators=[InputRequired()])
    submit = SubmitField("Logg inn")