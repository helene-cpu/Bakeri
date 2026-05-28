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

class BestilleForm(FlaskForm):
    epost = StringField("E-post", validators=[InputRequired()])
    antall = StringField("Antall Cupcakes", validators=[InputRequired()])
    smak = SelectField("Hvilken smak ønsker du?", choices=[
        ("---",""),
        ("Sjokolade", "Sjokolade"),
        ("Jordbær", "Jordbær"),
        ("Vanilje", "Vanilje"),
        ("Karamell", "Karamell"),
        ("Tutti Frutti", "Tutti Frutti")
    ], validators=[InputRequired()])
    topping = SelectField("Hva slags topping ønsker du?", choices=[
        ("---",""),
        ("Strøssel","Strøssel"),
        ("Oreo", "Oreo"),
        ("Godteri", "Godteri"),
        ("Ingenting", "Ingenting")
    ], validators=[InputRequired()])
    levering = StringField("Hvor ønsker du dette levert?", validators=[InputRequired()])
    submit = SubmitField("Send bestilling")

class AcceptForm(FlaskForm):
    svar = SelectField("Godkjenn eller bekreft ordre", choices=[
        ("---",""),
        ("Godkjent", "Godkjenn"),
        ("Ikke godkjent", "Avslå")
    ], validators=[InputRequired()])
    submit = SubmitField("Bekreft")