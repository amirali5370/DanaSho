from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
from passlib.hash import sha256_crypt
from models.user import User
from extentions import db

app = Blueprint("user" , __name__)


@app.route("/login", methods = ["POST","GET"])
def login():
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

        name = firstName + lastName


        user = User(name=name, username=username, password=sha256_crypt.encrypt(password), code=code, phone=phone, birth=birth, gender=gender, type=type, grade=grade)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("user.dashboard"))
    else:
        return render_template("user/login.html")
    

app.route("dashboard")
def dashboard():
    return "داشبورد"