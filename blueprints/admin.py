from flask import Blueprint, jsonify, render_template, request, send_file, session, redirect, abort, flash, url_for
from PIL import Image
import os
import config
import pandas as pd
from functions.methods import get_time, likes_calculator
from functions.text_generators import confirm_activate_text_generator, confirm_camp_text_generator, confirm_comment_text_generator, confirm_course_text_generator, reject_activate_text_generator, reject_comment_text_generator
from models.interaction import Interaction
from models.question import Question
from models.ticket import Ticket
from models.user import User
from models.book import Book
from extentions import db
from scoring import *

app = Blueprint("admin" , __name__)

@app.before_request
def before_request():
        if session.get("admin_login", None) == None and request.endpoint != "admin.login":
            abort(404)


##############################   ADMIN   ###############################
@app.route("/admin/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username',None)
        password = request.form.get('password',None)

        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session["admin_login"] = username
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("admin.login"))
    else:
        return render_template("admin/login.html")


@app.route("/admin/dashboard", methods = ["GET","POST"])
def dashboard():
    if request.method == "POST":
        grade = request.form.get('grade', None)
        file = request.files.get('file')
        file.save(f"static/files/{grade}.zip")

    return render_template("admin/dashboard.html")


@app.route('/admin/logout')
def logout():
    session.pop("admin_login", None)
    return redirect(url_for('admin.login'))


##############################   USER DATA   ###############################
@app.route("/admin/data", methods = ["GET", "POST"])
def data():
    if request.method == "POST":
        firstName = request.form.get("firstName", None)
        lastName = request.form.get("lastName", None)
        userName = request.form.get("userName", None)
        password = request.form.get("password", None)
        code = request.form.get("code", None)
        id_class = request.form.get("k_class", None)
        number = request.form.get("number", None)

        mode = request.form.get("mode")

        if mode == "add":
            u = User(firstName = firstName, lastName = lastName, username = userName, password = password, code = code, grade = "k_class.grade", field = "k_class.field", class_name = "k_class.name",  class_id = id_class, number = number)
            db.session.add(u)
            db.session.commit()

            flash('add success')
            return redirect(url_for('admin.students'))
        else:
            user = User.query.filter(User.id == int(mode)).first_or_404()
            user.firstName = firstName
            user.lastName = lastName
            user.username = userName
            user.password = password
            user.code = code
            user.class_id = id_class
            user.number = number

            user.grade = "k_class.grade"
            user.field = "k_class.field"
            user.class_name	= "k_class.name"

            db.session.commit()

            flash('edit success')
            return redirect(url_for('admin.students'))
    else:
        users = User.query.order_by(User.name).all()
        return render_template("admin/data.html", users=users)
    

@app.route("/admin/get_data")
def get_data():
    id = request.args.get("val", None)
    user = User.query.filter(User.id==id).first()
    gr = user.grade
    grade_code = 0 if gr == "teacher" else int(user.grade)
    data = {"username":user.username,
            "code":user.code,
            "phone":user.phone,
            "email":user.email,
            "grade":"دوره اول ابتدایی" if grade_code == 1 else "دوره دوم ابتدایی" if grade_code == 2 else "دوره متوسطه اول" if grade_code == 3 else "دوره متوسطه دوم" if grade_code == 4 else "فرهنگی",
            "birth":user.birth,
            "gender":user.gender,
            "type":user.type,
            "invite_code":user.invite_code,
            "province":user.province,
            "city":user.city,
            "school_name":user.school_name,
            "school_type":user.school_type,
            "home_addres":user.home_addres,
            "recognition":user.recognition,
            "final":"انجام شده" if user.final == 1 else "انجام نشده",
            "authentication":"انجام شده" if user.authentication == 1 else "انجام نشده",
            "downloads":user.downloads,
            "coin":user.coin,
            "point":user.point,
            "badge":user.badge,
            "like" :user.like,
            "invite" :user.invite}
    return jsonify(data)
    

@app.route("/admin/change_data")
def change_data():
    id = request.args.get("val")
    coin = request.args.get("coin")
    point = request.args.get("point")
    badge = request.args.get("badge")
    downloads = request.args.get("downloads")
    user = User.query.filter(User.id==id).first()
    user.coin = coin
    user.point = point
    user.badge = badge
    user.downloads = downloads
    db.session.commit()
    return jsonify({'status':200})


##############################   BOOKS   ###############################
@app.route("/admin/books", methods=["GET","POST"])
def books():
    if request.method == "POST":
        name = request.form.get("name", None)
        about = request.form.get("about", None)
        grade = request.form.get("grade", None)
        primalink = request.form.get("primalink", None)
        mode = request.form.get("mode", None)
        if mode=="add":
            file = request.files.get("photo", None)

            b = Book(name=name, about=about, grade=grade, primalink=primalink)
            db.session.add(b)
            db.session.commit()

            file.save(f"static/books/{file.filename}")

            image = Image.open(f"static/books/{file.filename}")
            resized_image = image.resize(vol_size)
            resized_image = resized_image.convert("RGB") 
            resized_image.save(f"static/books/{b.id}.jpg", 'JPEG')

            os.remove(f"static/books/{file.filename}")

            flash('book_add_success')
            return redirect(url_for('admin.books'))
        
        else:
            b = Book.query.filter(Book.id==int(mode)).first_or_404()
            b.name = name
            b.about = about
            b.grade = grade
            db.session.commit()
            flash('book_edit_success')
            return redirect(url_for('admin.books'))
    else:
        books = Book.query.order_by(Book.grade).all()
        return render_template("admin/books.html", books=books)
    

@app.route("/admin/del-book/<id>", methods = ["GET", "POST"])
def delete_book(id):
    status = request.args.get("status")
    if status == "true":
        book = Book.query.filter(Book.id == id).first_or_404()
        
        interactions = Interaction.query.filter(Interaction.book_id==book.id).all()
        for i in interactions:
            db.session.delete(i)
        # آزمون ها هم حذف شوند

        db.session.delete(book)
        db.session.commit()
        os.remove(f"static/books/{book.id}.jpg")
        flash('book_del_success')
    return redirect(url_for("admin.books"))

@app.route("/admin/photo-book/<id>", methods = ["GET", "POST"])
def edit_photo_book(id):
    file = request.files.get("photo", None)
    if file!=None:
        file.save(f"static/books/{file.filename}")

        image = Image.open(f"static/books/{file.filename}")
        resized_image = image.resize(vol_size)
        resized_image = resized_image.convert("RGB") 
        resized_image.save(f"static/books/{id}.jpg", 'JPEG')

        os.remove(f"static/books/{file.filename}")
        
    flash('book_edit_success')
    return redirect(url_for('admin.books'))
################## cofirmation ##################
#comment
@app.route("/admin/comments")
def comments():
    comments = Interaction.query.filter(Interaction.type != 'activism',Interaction.status == 'review').all()
    return render_template("admin/comments.html", comments=comments)

@app.route("/admin/comments-api", methods=["POST","GET"])
def comment_api():
    if request.method == "GET":
        abort(404)
    status = request.form.get('status', None)
    if status=="confirmed" or status=="rejected":
        comment_id = request.form.get('comment', None)
        comment = Interaction.query.filter(Interaction.id==comment_id).first_or_404()
        comment.status = status
        if status=="confirmed" and comment.type=="comment":
            comment.user.coin += coin_04
            text = confirm_comment_text_generator(comment)
            tic = Ticket(type='comment_sta', sub_type='comment', content=text, user_id=comment.user_id, time=get_time())
            db.session.add(tic)
        elif status=="rejected" and comment.type=="comment":
            text = reject_comment_text_generator(comment)
            tic = Ticket(type='comment_sta', sub_type='comment', content=text, user_id=comment.user_id, time=get_time())
            db.session.add(tic)
        db.session.commit()
        return jsonify({'status':'200'})
    else:
        abort(404)

#activism
@app.route("/admin/activisms")
def activisms():
    activisms = Interaction.query.filter(Interaction.type == 'activism',Interaction.status == 'review').all()
    return render_template("admin/activisms.html", activisms=activisms)

@app.route("/admin/activisms-api", methods=["POST"])
def activism_api():
    if request.method == "GET":
        abort(404)
    status = request.form.get('status', None)
    if status=="confirmed" or status=="rejected":
        activism_id = request.form.get('activism', None)
        activism = Interaction.query.filter(Interaction.id==activism_id).first_or_404()
        activism.status = status

        if status=="confirmed" and activism.type=="activism":
            text = confirm_activate_text_generator(activism)
            activism.user.point += point_02
        elif status=="rejected" and activism.type=="activism":
            text = reject_activate_text_generator(activism)

        tic = Ticket(type='comment_sta', sub_type='activism', content=text, user_id=activism.user_id, time=get_time())
        db.session.add(tic)
        db.session.commit()
        return jsonify({'status':'200'})
    else:
        abort(404)

#requests
@app.route("/admin/requests")
def requests():
    requests = Ticket.query.filter(Ticket.type == 'request',Ticket.status == 'review').all()
    return render_template("admin/requests.html", requests=requests)

@app.route("/admin/requests-api", methods=["POST"])
def request_api():
    if request.method == "GET":
        abort(404)
    status = request.form.get('status', None)
    if status=="confirmed" or status=="rejected":
        request_id = request.form.get('request', None)
        requested = Ticket.query.filter(Ticket.id==request_id).first_or_404()
        requested.status = status

        if status=="confirmed" and requested.sub_type=="camp":
            text = confirm_camp_text_generator(requested.user.name)
            requested.user.coin += coin_06
            tic = Ticket(type='coin_confirm', sub_type=requested.type, content=text, user_id=requested.user_id, time=get_time())
            db.session.add(tic)
        elif status=="confirmed" and requested.sub_type=="course":
            text = confirm_course_text_generator(requested.user.name)
            requested.user.coin += coin_05
            tic = Ticket(type='coin_confirm', sub_type=requested.type, content=text, user_id=requested.user_id, time=get_time())
            db.session.add(tic)

        db.session.commit()
        return jsonify({'status':'200'})
    else:
        abort(404)

##############################   Quiz   ###############################
@app.route("/admin/quiz/<book_link>", methods=["GET","POST"])
def quiz(book_link):
    book = Book.query.filter(Book.primalink==book_link).first_or_404()
    if request.method == "POST":
        book.number = file = request.form['number']
        book.time = file = request.form['time']
        db.session.commit()

        file = request.files['file']
        if file!=None:
            if file.filename != '':
                df = pd.read_excel(file)
                q_old = Question.query.filter(Question.book_id == book.id).all()
                for i in q_old:
                    db.session.delete(i)
                    db.session.commit() 

                for index, row in df.iterrows():
                    q = Question(book_id=book.id, text=row['text'], option1=row['op1'], option2=row['op2'], option3=row['op3'], option4=row['op4'])
                    q.answer = q.__dict__['option' + str(row['answer'])]
                    db.session.add(q)
                
                db.session.commit()

            flash('quiz_add_success')
        return redirect(url_for('admin.quiz', book_link=book_link))
    else:
        questions = Question.query.filter(Question.book_id == book.id).all()
        return render_template("admin/questions.html", questions=questions, book=book)
    
#########################################################################

@app.route('/admin/likes_calculator')
def like_cal():
    users = User.query.all()
    for u in users:
        u.like = likes_calculator(u)
    db.session.commit()
    return '200'

@app.route('/admin/question_file')
def question_file():
    path = "static/files/Questions.xlsx"
    return send_file(path, as_attachment=True)
    
