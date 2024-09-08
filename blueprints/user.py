from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from passlib.hash import sha256_crypt
from models.user import User
from models.invite import Invite
from models.payment import Payment
from extentions import db
from functions.methods import invite_generator
from sqlalchemy.exc import IntegrityError
from instance.data import cities as city_data
from instance.data import school_types, recognitions
from scoring import *
import requests
import json

app = Blueprint("user" , __name__)

# ------------- LOGIN AND REGISTER-------------
#register page
@app.route("/register", methods = ["POST","GET"])
def register():
    next = request.args.get('next',None)
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
                inviter.point = inviter.point + 30
                db.session.add(inv)
                inviter.invite = len(Invite.query.filter(Invite.inviter_id==inviter.id).all())
                db.session.commit()

        login_user(user)
        if next != None:
            return redirect(next)
        return redirect(url_for("user.dashboard"))
    else:
        return render_template("user/register.html")
    
#login page
@app.route("/login", methods = ["POST","GET"])
def login():
    next = request.args.get('next',None)
    if request.method == "POST":

        username = request.form.get('username',None)
        password = request.form.get('password',None)


        user = User.query.filter(User.username==username).first()
        if user == None:
            flash("نام کاربری یا رمز عبور اشتباه است!")
            return redirect(request.url)
        
        elif sha256_crypt.verify(password, user.password):
            login_user(user)
            if next != None:
                return redirect(next)
            return redirect(url_for("user.dashboard"))
        

        else:
            flash("نام کاربری یا رمز عبور اشتباه است!")
            return redirect(request.url)



    else:
        return render_template("user/login.html", next=next)
    
#logout link
@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('general.main'))


# ------------- COMPLETION -------------
#completion page
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
    

# ------------- PAYMENT-------------
#payment handler
@app.route("/payment", methods=["GET"])
@login_required
def payment():
    next = request.args.get('next',None)
    if current_user.final != 0:
        if next != None:
            return redirect(next)
        return redirect(url_for("user.dashboard"))
    r = requests.post('https://sandbox.shepa.com/api/v1/token', 
                    data={
                        'api':'sandbox',
                        'amount':price,
                        'callback':str(url_for('user.verify', _external=True))
                    })
    
    token = r.json()['result']['token']
    url = r.json()['result']['url']

    pay = Payment(user_id=current_user.id, token=token, next=next, amount=price)
    db.session.add(pay)
    db.session.commit()

    return redirect(url)

#verify handler
@app.route("/verify", methods=["GET"])
def verify():
    token = request.args.get('token')
    pay = Payment.query.filter(Payment.token==token).first_or_404()
    r = requests.post('https://sandbox.shepa.com/api/v1/verify', 
                    data={
                        'api':'sandbox',
                        'amount':pay.amount,
                        'token':token
                    })
    status = bool(r.json()['success'])
    if status:
        flash("payment_success")

        pay.status = "success"
        pay.card_pan = r.json()['result']['card_pan']
        pay.date = r.json()['result']['date']
        pay.refid = r.json()['result']['refid']
        pay.transaction_id = r.json()['result']['transaction_id']
        pay.user.final = 1
        pay.user.coin = pay.user.coin + coin_02
        db.session.commit()
    else:
        flash("payment_failed")

        pay.status = "failed"
        pay.error = r.json()['error'][0]
        db.session.commit()
    if pay.next != None:
        return redirect(pay.next)
    return redirect(url_for("user.dashboard"))



# ------------- MORE API-------------
@app.route('/get_cities/<province>')
def get_cities(province):
    cities = city_data.get(province, [])
    return jsonify(cities)


# ------------- MAIN-------------
#dashboard page
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("user/dashboard.html", user=current_user)

#club page
@app.route('/club')
@login_required
def club():
    top_coins = User.query.order_by(User.coin.desc()).limit(10).all()
    top_points = User.query.order_by(User.point.desc()).limit(10).all()
    top_likes = User.query.order_by(User.like.desc()).limit(10).all()
    top_badges = User.query.order_by(User.badge.desc()).limit(10).all()
    top_invites = User.query.order_by(User.invite.desc()).limit(10).all()

    rank_coins = User.query.order_by(User.coin.desc()).all().index(current_user)+1
    rank_points = User.query.order_by(User.point.desc()).all().index(current_user)+1
    rank_likes = User.query.order_by(User.like.desc()).all().index(current_user)+1
    rank_badges = User.query.order_by(User.badge.desc()).all().index(current_user)+1
    rank_invites = User.query.order_by(User.invite.desc()).all().index(current_user)+1

    province_rank = User.query.filter(User.province==current_user.province).order_by(User.point.desc()).all().index(current_user)+1
    city_rank = User.query.filter(User.city==current_user.city).order_by(User.point.desc()).all().index(current_user)+1

    return render_template("user/club.html", user=current_user, top_coins=top_coins, top_points=top_points, top_likes=top_likes, top_badges=top_badges, top_invites=top_invites,
                           rank_coins=rank_coins, rank_points=rank_points, rank_likes=rank_likes, rank_badges=rank_badges, rank_invites=rank_invites,
                            province_rank=province_rank, city_rank=city_rank)

#club page
@app.route('/invites')
@login_required
def invites():
    invitees = current_user.invites.all()
    return render_template("user/invites.html", user=current_user, invitees=invitees)