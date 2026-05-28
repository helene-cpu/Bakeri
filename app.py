from flask import Flask, render_template, redirect, session, request
import mysql.connector
import sendgrid
from forms import LoginForm, RegisterForm, BestilleForm, AcceptForm
from werkzeug.security import check_password_hash, generate_password_hash
from config import DB_Password
from sendgrid.helpers.mail import Mail


app = Flask(__name__)
app.config["SECRET_KEY"] = "superduperekstrahemmelig123"

def get_conn():
    return mysql.connector.connect(
        host = "localhost",
        user = "baker",
        password = DB_Password,
        database = "Bakeri"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bestill', methods=["POST", "GET"])
def bestill():
    form = BestilleForm()
    epost = form.epost.data
    antall = form.antall.data
    smak = form.smak.data
    topping = form.topping.data
    levering = form.levering.data

    if form.validate_on_submit():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO bestilling (Epost, Antall, Smak, Topping, Levering) values (%s, %s, %s, %s, %s)",
            (epost, antall, smak, topping, levering)
        )
        conn.commit()
        cur.close()
        conn.close()

        return render_template('bestilt.html', form=form)

    return render_template('bestill.html', form=form)

@app.route('/bestilt', methods=["POST", "GET"])
def bestilt():
    return render_template("bestilt.html")

@app.route('/admin', methods=["POST", "GET"])
def admin():
    form = AcceptForm()
    svar = form.svar.data


    return render_template("admin.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        brukernavn = form.brukernavn.data
        passord = form.passord.data 

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT Navn, Passord FROM brukere WHERE Brukernavn= %s",
            (brukernavn,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            navn_db = user[0]
            passord_db = user[1]

            if check_password_hash(passord_db, passord):
                session['navn'] = navn_db
                return redirect("/admin")
    
            else:
                form.brukernavn.errors.append("Feil brukernavn eller passord")

        else:
            form.brukernavn.errors.append("Feil brukernavn eller passord")

    return render_template('login.html', form = form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        navn = form.navn.data
        brukernavn = form.brukernavn.data
        passord = form.passord.data

        passord_hash = generate_password_hash(passord)

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO brukere (Navn, Brukernavn, Passord) VALUES (%s, %s, %s)",
            (navn, brukernavn, passord_hash)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run()