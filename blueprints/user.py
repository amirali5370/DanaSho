from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from passlib.hash import sha256_crypt
from models.user import User
from models.invite import Invite
from extentions import db
from functions.methods import invite_generator
from sqlalchemy.exc import IntegrityError
from instance.data import cities as city_data
from instance.data import school_types, recognitions
from scoring import *

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
        email = request.form.get('email',None)
        invite = request.form.get('invite',None)


        name = firstName + " " + lastName
        invite_code = invite_generator()


        user = User(name=name, username=username, password=sha256_crypt.encrypt(password), code=code, phone=phone, birth=birth, gender=gender, type=type, grade=grade, invite_code=invite_code, email=email)
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
                inviter.invite = len(Invite.query.filter(Invite.inviter_id==inviter.id).all())
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
            return redirect(request.url)
        
        elif sha256_crypt.verify(password, user.password):
            login_user(user)
            next = request.args.get('next',None)
            if next != None:
                return redirect(next)
            return redirect(url_for("user.dashboard"))
        

        else:
            flash("نام کاربری یا رمز عبور اشتباه است!")
            return redirect(request.url)



    else:
        return render_template("user/login.html")
    

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('general.main'))



@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("user/dashboard.html")


@app.route("/completion", methods=["GET","POST"])
@login_required
def completion():
    next = request.args.get('next',None)
    if current_user.completion != 0:
        if next != None:
            return redirect(next)
        return redirect(url_for("user.dashboard"))
    if request.method == "POST":

        province = request.form.get('province',None)
        city = request.form.get('city',None)
        school_name = request.form.get('school_name',None)
        school_type = request.form.get('school_type',None)
        addres = request.form.get('addres',None)
        recognition = request.form.get('recognition',None)

        user = current_user

        school_type = school_types[school_type]
        recognition = recognitions[recognition]
        print(city,province)

        user.province = province
        user.city = city
        user.school_name = school_name
        user.school_type = school_type
        user.home_addres = addres
        user.recognition = recognition
        user.completion = 1

        user.coin = user.coin + coin_01

        db.session.commit()


        if next != None:
            return redirect(next)
        return redirect(url_for("user.dashboard"))

    else:
        return render_template("user/completion.html")
    

@app.route('/get_cities/<province>')
def get_cities(province):
    cities = city_data.get(province, [])
    return jsonify(cities)