from flask import Blueprint, abort, render_template, request, redirect, send_file, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from passlib.hash import sha256_crypt
from functions.methods import is_liked, get_time
import os
import math
import time
import random
from PIL import Image
from models.book import Book
from models.question import Question
from models.result import Result
from models.ticket import Ticket
from models.user import User
from models.invite import Invite
from models.payment import Payment
from models.interaction import Interaction
from models.like import Like
from extentions import db
from functions.code_generators import authCode_generator, invite_generator, inviteAuth_generator
from functions.text_generators import *
from sqlalchemy.exc import IntegrityError
from instance.data import cities as city_data
from instance.data import *
from scoring import *
import requests

app = Blueprint("user" , __name__)

# ------------- LOGIN AND REGISTER-------------
#register page
@app.route("/register", methods = ["POST","GET"],  strict_slashes=False)
def register():
    next = request.args.get('next',None)
    inv = request.args.get('invite',None)
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
        province = request.form.get('province',None)
        city = request.form.get('city',None)
        school_name = request.form.get('school_name',None)
        school_type = request.form.get('school_type',None)
        addres = request.form.get('addres',None)
        recognition = request.form.get('recognition',None)

        if type == "teacher":
            grade = 0

        user = current_user

        school_type = school_types[school_type]
        recognition = recognitions[recognition]



        name = firstName + " " + lastName
        invite_code = invite_generator()
        invite_auth = inviteAuth_generator()


        user = User(name=name, username=username, password=sha256_crypt.encrypt(password), code=code, phone=phone, birth=birth, gender=genders[gender], type=types[type], grade=grade, invite_code=invite_code, invite_auth=invite_auth, email=email)
        
        user.province = province
        user.city = city
        user.school_name = school_name
        user.school_type = school_type
        user.home_addres = addres
        user.recognition = recognition
        


        if inv != None:
            inviter = User.query.filter(User.invite_auth==inv).first()
        else:
            inviter = User.query.filter(User.invite_code==invite).first()

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            flash("unique")
            return redirect(request.url)

        if inviter != None:
                inv = Invite(inviter_id=inviter.id , invitee_id=user.id , invitee=name)
                inviter.point = inviter.point + point_01
                db.session.add(inv)
                inviter.invite = len(Invite.query.filter(Invite.inviter_id==inviter.id).all())
                tik = Ticket(type="invited", content=invited_text_generator(inviter.name, user.name), user_id=inviter.id, time=get_time())
                db.session.add(tik)
                db.session.commit()

        login_user(user)
        if next != None:
            return redirect(next)
        return redirect(url_for("user.home"))
    else:
        if inv != None:
            inviting = False
        else:
            inviting = True
        return render_template("user/register.html", inviting=inviting, recognitions=recognitions, provinces=cities.keys(), next=next)
    
#login page
@app.route("/login", methods = ["POST","GET"],  strict_slashes=False)
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
            return redirect(url_for("user.home"))
        

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
    return redirect(url_for('user.home'))

#get city api
@app.route('/get_cities')
def get_cities():
    province = request.args.get('province' , None)
    if province == None:
        abort(404)
    cities = city_data.get(province, [])
    return jsonify(cities)


# ------------- HOME -------------

#home user page
@app.route("/",  strict_slashes=False)
def home():
    books = Book.query.all()
    return render_template("user/home.html", books=books)

#comments (single book page)
@app.route("/book/<book_link>", methods=["GET","POST"],  strict_slashes=False)
def book(book_link):
    book = Book.query.filter(Book.primalink==book_link).first_or_404()
    if request.method == "POST":
        comment = request.form.get('comment' , None)
        print(request.form)
        c = Interaction(type="comment", content=comment, user_id=current_user.id, book_id=book.id, time=get_time())
        db.session.add(c)

        tik = Ticket(type="comment_sta", sub_type="review", content=review_comment_text_generator(current_user.name), user_id=current_user.id, time=get_time())
        db.session.add(tik)

        db.session.commit()
        flash("comment_add_success")
        return redirect(request.url)
        
    else:
        comments = book.interactions.filter(Interaction.type=="comment", Interaction.status=="confirmed").all()
    
        return render_template("user/book.html", book=book, comments=comments)



# ------------- ACTIVISM -------------

#activism (single book page)
@app.route("/activism", methods=["GET","POST"],  strict_slashes=False)
@login_required
def activism():
    books = Book.query.filter(Book.grade==current_user.grade).all()
    return render_template("user/activism.html", books=books)


#activism (single book page)
@app.route("/activism/<book_link>", methods=["GET","POST"],  strict_slashes=False)
@login_required
def book_activisms(book_link):
    book = Book.query.filter(Book.primalink==book_link).first_or_404()
    if request.method == "POST":
        replay_id = request.form.get('replay_id' , None)
        if replay_id==None:
            activism = request.form.get('activism' , None)
            file = request.files.get("photo", None)
            c = Interaction(type="activism", content=activism, user_id=current_user.id, book_id=book.id, time=get_time())
            db.session.add(c)
            db.session.commit()
            print(c.id)
            
            file.save(f"static/activisms/{file.filename}")

            image = Image.open(f"static/activisms/{file.filename}")
            resized_image = image.resize(vol_size)
            resized_image = resized_image.convert("RGB") 
            resized_image.save(f"static/activisms/{c.id}.jpg", 'JPEG')

            os.remove(f"static/activisms/{file.filename}")
            
            tik = Ticket(type="activism_sta", sub_type="review", content=review_activate_text_generator(current_user.name), user_id=current_user.id, time=get_time())
            db.session.add(tik)

            db.session.commit()
            flash("activism_add_success")
            return redirect(request.url)
        else:
            comment = request.form.get('comment' , None)
            c = Interaction(type="replay", content=comment, user_id=current_user.id, book_id=book.id, replay=replay_id, time=get_time())
            db.session.add(c)
            db.session.commit()
            flash("replay_add_success")
            return redirect(request.url)
        
    else:
        activisms = book.interactions.filter(Interaction.type=="activism", Interaction.status=="confirmed").all()
        replays = book.interactions.filter(Interaction.type=="replay", Interaction.status=="confirmed").all()
        return render_template("user/single-activism.html", book=book, activisms=activisms, replays=replays)

@app.route("/like_maneger", methods=["POST"])
@login_required
def like_maneger():
    user_id = request.form.get('user_id' , None)
    activism_id = request.form.get('activism_id' , None)
    user = User.query.filter(User.id==user_id).first_or_404()
    if user == current_user:
        activism = Interaction.query.filter(Interaction.id==activism_id).first_or_404()
        like = is_liked(user,activism)

        if like:
            l = Like.query.filter(Like.user_id==user.id, Like.activism_id==activism.id).first_or_404()
            db.session.delete(l)
            db.session.commit()
            return jsonify({"status":200})
        else:
            l = Like(user_id=current_user.id,activism_id=activism.id)
            db.session.add(l)
            db.session.commit()
            return jsonify({"status":200})
    else:
        abort(404)


#quiz
@app.route("/quiz/<book_link>", methods=["GET","POST"],  strict_slashes=False)
@login_required
def book_quiz(book_link):
    book = Book.query.filter(Book.primalink==book_link).first_or_404()
    r = Result.query.filter(Result.user_id==current_user.id, Result.book_id==book.id).first()
    print(r)           
    if book.number == 0:
        abort(404)

    if request.method == "POST":

        true = 0

        for key, value in request.form.items():
            if key != 'csrf_token':
                q = Question.query.filter(Question.id==key[1:]).first()
                print(q.answer, value)
                if q.answer == value:
                    true += 1
        result = true*100/book.number
        print(result)
        if r.score < result:
            ol_p =  math.ceil((r.score/100)*point_04)
            new_p =  math.ceil((result/100)*point_04)
            p = new_p - ol_p
            r.score = result
            current_user.point += p
        else:
            p = 0
        db.session.commit()
                
        flash(f'{p} امتیاز')
        return redirect(url_for('user.book_activisms', book_link=book.primalink))
     
    else:
        if r==None:
            r = Result(user_id=current_user.id, book_id=book.id)
            db.session.add(r)
            db.session.commit()

        if r.enter > 1:
            flash('quiz_more_2')
            return redirect(url_for('user.book_activisms', book_link=book.primalink)) 
        
        r.enter = r.enter+1
        db.session.commit()
        
        questions = random.sample(book.questions.all(), book.number)
        return render_template("user/quiz.html", book=book, questions=questions)







# ------------- CLUB -------------

#club page
@app.route('/club',  strict_slashes=False)
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

    return render_template("user/club.html", top_coins=top_coins, top_points=top_points, top_likes=top_likes, top_badges=top_badges, top_invites=top_invites,
                           rank_coins=rank_coins, rank_points=rank_points, rank_likes=rank_likes, rank_badges=rank_badges, rank_invites=rank_invites,
                            province_rank=province_rank, city_rank=city_rank)



# ------------- PROFILE -------------
@app.route("/profile", methods=["GET","POST"],  strict_slashes=False)
@login_required
def profile():
    if request.method == "POST":
        file = request.files.get("file", None)

        file.save(f"static/users/{file.filename}")
        image = Image.open(f"static/users/{file.filename}")
        resized_image = image.resize((280, 280))
        resized_image = resized_image.convert("RGB") 
        resized_image.save(f"static/users/{current_user.id}.jpg", 'JPEG')

        os.remove(f"static/users/{file.filename}")

        return redirect(request.url)
    else:
        activisms = len(current_user.interactions.filter(Interaction.type=='activism', Interaction.status=='confirmed').all())
        comments = len(current_user.interactions.filter(Interaction.type=='comment', Interaction.status=='confirmed').all())
        return render_template("user/profile.html", activisms=activisms, comments=comments)
    
#books' file
@app.route('/download')
@login_required
def download_file():
    if current_user.authentication == 1 and current_user.final == 1:
        if current_user.downloads > 0:
            path = f"static/files/{current_user.grade}.zip"
            current_user.downloads += -1
            db.session.commit()
            return send_file(path, as_attachment=True)
    abort(403)


#  ||||||||||||||||   completion   ||||||||||||||
#completion page
@app.route("/completion", methods=["GET"],  strict_slashes=False)
@login_required
def completion():
    next = request.args.get('next',None)
    authentication = True if current_user.authentication != 0 else False
    final = True if current_user.final != 0 else False

    if authentication and final:
        if next != None:
            return redirect(next)
        return redirect(url_for("user.home"))

    else:
        return render_template("user/completion.html", final=final, authentication=authentication, price=price, next=next)

#authentication api
@app.route("/authentication")
@login_required
def authentication():
    auth = request.args.get('auth',None)
    if current_user.invite_auth == auth:
        if current_user.authentication == 0:
        
            code = authCode_generator()

            # r = requests.post("https://api.payamak-panel.com/post/Send.asmx")
            # if r.status_code == 200:
            current_user.msg_code = code
            db.session.commit()
            return jsonify({"status":"200"})
        else:
            return redirect(url_for('user.completion'))
    else:
        abort(403)
    
#confirmation handler
@app.route("/confirmation", methods=["GET"])
@login_required
def confirmation():
    code = int(request.args.get('code',None))
    if code == current_user.msg_code :
        current_user.authentication = 1
        current_user.coin = current_user.coin + coin_01
        current_user.msg_code = None
        db.session.commit()
        flash("confirmation_suc")
        return jsonify({"status":"200"})
    else:
        flash("confirmation_fil")
        return jsonify({"status":"404"})

#confirmation code deleter
@app.route("/unconf", methods=["GET"])
@login_required
def unconf():
    auth = request.args.get('auth',None)
    if current_user.invite_auth == auth:
        current_user.msg_code = None
        db.session.commit()
        return jsonify({"status":"200"})
    abort(404)

#payment handler
@app.route("/payment", methods=["GET"])
@login_required
def payment():
    next = request.args.get('next',None)
    if current_user.final != 0:
        if next != None:
            return redirect(next)
        return redirect(url_for("user.home"))
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
    next = '?next='+pay.next if pay.next != None else ""
    return redirect(url_for("user.completion")+next)

#  ||||||||||||||||   invite   ||||||||||||||
#invites page
@app.route('/invites',  strict_slashes=False)
@login_required
def invites():
    invitees = current_user.invites.order_by(Invite.id.desc()).limit(10).all()
    inv = current_user.invites.all()
    return render_template("user/invites.html", invitees=invitees, inv=inv)


# ------------- TICKET -------------

#ticket page
@app.route("/ticket",  strict_slashes=False)
@login_required
def ticket():
    tickets = current_user.tickets.order_by(Ticket.id.desc()).all()
    return render_template("user/ticket.html", tickets=tickets)

#ticket api
@app.route("/ticket_add", methods=["POST"])
@login_required
def ticket_add():
    user_id = request.form.get('user_id', None)
    user = User.query.filter(User.id==user_id).first_or_404()
    if user==current_user:
        req = request.form.get('type', None)
        req = "camp" if req=="or" else "course"
        text = camp_req_text_generator(current_user.name) if req=="camp" else course_req_text_generator(current_user.name)
        tik = Ticket(type="request", sub_type=req, content=text, user_id=current_user.id, time=get_time(), status='review')
        db.session.add(tik)
        db.session.commit()
        return '200'
    else:
        abort(404)
    
    return render_template("user/ticket.html")
