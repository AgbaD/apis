#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

# package
from flask import *
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# user created
from . import main
from .. import db
from ..models import User
from ..utilities.email_sender import send_mail
from ..utilities.schema import validate_login, validate_reg

# system
import re
import uuid


@main.route("/register")
def register():
    return render_template("register.html")   # display register user of vendor


@main.route("/register/user", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        phone = request.form.get("phone")
        address = request.form.get("address")

        data = {
            "firstname": firstname, "lastname": lastname,
            "email": email, "password": password, "phone": str(phone)
        }

        if password != repeat_password:
            flask("Passwords do not match!")
            return render_template("register_user.html", data=data)

        schema_result = validate_reg(data)
        if schema_result["msg"] != "success":
            flash(schema_result['error'])
            return render_template("register_user.html", data=data)
        if User.query.filter_by(email=email).first():
            flash("Email already registered!")
            return render_template("register_user.html", data=data)
        if not re.fullmatch(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email):
            flash('Enter valid email')
            return render_template("register_user.html", data=data)

        public_id = str(uuid.uuid4())
        role = "user"
        password_hash = generate_password_hash(password)

        user = User(email=email, firstname=firstname, lastname=lastname,
                    phone=phone, public_id=public_id, password=password_hash,
                    address=address, role=role)
        db.session.add(user)
        db.session.commit()

        # create confirmation token
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'confirm': user.public_id})

        send_mail("Account Confirmation", email/auth/confirm, user.email, user=user, token=token)
        flash("Please check you email to confirm your account!")
        return redirect(url_for('main.login'))
    return render_template("register_user.html")


@main.route("/confirm_token/<token>")
@login_required
def confirm_token(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.index'))
    if data.get('confirm') != current_user.public_id:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.index'))
    current_user.confirmed = True
    db.session.add(current_user)
    return redirect(url_for('main.index'))


@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember')

        data = {"email": email, "password": password}

        schema_result = validate_login(data)
        if schema_result["msg"] != "success":
            flash(schema_result['error'])
            return render_template("login.html", data=data)

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Account not found please check email.")
            return render_template("login.html", data=data)
        if not check_password_hash(user.password_hash, password):
            flash("Password incorrect!")
            return render_template("login.html", data=data)
        login_user(user, remember_me)
        return redirect(url_for("main.index"))
    return render_template('login.html')


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


