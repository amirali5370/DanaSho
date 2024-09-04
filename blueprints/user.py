from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from passlib.hash import sha256_crypt
from models.user import User
from models.invite import Invite
from extentions import db
from functions.methods import invite_generator
from sqlalchemy.exc import IntegrityError

app = Blueprint("user" , __name__)


@app.route("/register", methods = ["POST","GET"])
def register():
    if request.method == "POST":
        firstName = request.form.get('firstname',None)
        lastName = request.form.get('lastname',None)
        username = request.form.get('username',None)
        password = request.form.get('password',None)
        code = request.form.get('code',None)
        phone = request.form.get('phone',None)
        birth = request.form.get('birth',None)
        gender = request.form.get('gender',None)
        type = request.form.get('type',None)
        grade = request.form.get('grade',None)
        invite = request.form.get('invite',None)


        name = firstName + " " + lastName
        invite_code = invite_generator()


        user = User(name=name, username=username, password=sha256_crypt.encrypt(password), code=code, phone=phone, birth=birth, gender=gender, type=type, grade=grade, invite_code=invite_code)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            flash("unique")
            return redirect(url_for("user.register"))

        inviter = User.query.filter(User.invite_code==invite).first()
        if inviter != None:
                inv = Invite(inviter_id=inviter.id , invitee_id=user.id , invitee=name)
                db.session.add(inv)
                db.session.commit()

        login_user(user)
        
        return redirect(url_for("user.dashboard"))
    else:
        return render_template("user/register.html")
    

@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":

        username = request.form.get('username',None)
        password = request.form.get('password',None)


        user = User.query.filter(User.username==username).first()
        if user == None:
            flash("نام کاربری یا رمز عبور اشتباه است!")
            return redirect(url_for("user.login"))
        
        elif sha256_crypt.verify(password, user.password):
            login_user(user)
            return redirect(url_for("user.dashboard"))
        else:
            flash("نام کاربری یا رمز عبور اشتباه است!")
            return redirect(url_for("user.login"))



    else:
        return render_template("user/login.html")
    

@app.route("/dashboard")
def dashboard():

    return "داشبورد"