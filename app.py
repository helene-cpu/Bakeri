from flask import Flask, render_template, redirect, session, request
import mysql.connector
import sendgrid
from forms import LoginForm, RegisterForm, BestilleForm, AcceptForm
from werkzeug.security import check_password_hash, generate_password_hash
from config import DB_Password
from sendgrid.helpers.mail import Mail
from config import SENDGRID_API_KEY, SENDGRID_FROM_EMAIL


app = Flask(__name__)
app.config["SECRET_KEY"] = "superduperekstrahemmelig123"

def get_conn():
    return mysql.connector.connect(
        host = "localhost",
        user = "baker",
        password = DB_Password,
        database = "Bakeri"
)

def send_email(til_epost, antall, smak, topping, levering):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL, 
        to_emails=til_epost,
        subject="Bestillingen din er bekreftet!"
    )

    message.template_id = "d-1e763544b9d94926a8fdf01e92699066"

    message.dynamic_template_data = {
        "Antall": antall,
        "Smak": smak,
        "Topping": topping,
        "Levering": levering
    }
    sg.send(message)

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

        return redirect("/bestilt")

    return render_template('bestill.html', form=form)

@app.route('/bestilt', methods=["POST", "GET"])
def bestilt():
    return render_template("bestilt.html")

@app.route('/admin', methods=["POST", "GET"])
def admin():
    form = AcceptForm()
    if form.validate_on_submit():
        svar = form.svar.data
        bestilling_id = request.form.get('bestilling_id')

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
           "UPDATE bestilling SET Svar = %s WHERE Bestilling_ID = %s",
           (svar, bestilling_id)
        )

        conn.commit()
        cur.execute(
            "SELECT epost, Antall, Smak, Topping, Levering FROM bestilling WHERE Bestilling_ID = %s",
            (bestilling_id,)
        )
        ordre = cur.fetchone()
        cur.close()
        conn.close()

        if svar == "Godkjent":
            send_email(ordre[0], ordre[1], ordre[2], ordre[3], ordre[4])

        return redirect("/admin")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT epost, Antall, Smak, Topping, Levering, Bestilling_ID FROM bestilling WHERE Svar IS NULL"
    )

    ordre = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("admin.html", ordre=ordre, form=form)

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

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/manual')
def manual():
    return render_template("manual.html")

if __name__ == "__main__":
    app.run(debug=True)