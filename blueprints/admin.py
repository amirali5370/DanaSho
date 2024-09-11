from flask import Blueprint, jsonify, render_template, request, session, redirect, abort, flash, url_for
import os
import config
from models.user import User
from models.book import Book
from extentions import db

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


@app.route("/admin/dashboard", methods = ["GET"])
def dashboard():
    return render_template("admin/dashboard.html")


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
        users = User.query.all()
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
        mode = request.form.get("mode", None)
        if mode=="add":
            file = request.files.get("photo", None)

            b = Book(name=name, about=about, grade=grade)
            db.session.add(b)
            db.session.commit()
            file.save(f"static/books/{b.id}.jpg")

            flash('book_add_success')
            return redirect(url_for('admin.books'))
        
        else:
            b = Book.query.filter(Book.id==int(mode)).first_or_404()
            b.name = name
            b.about = about
            b.grade = grade
            #TODO:  عکس هم ویرایش شود
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
        # TODO : کنش ها و آزمون هایش حدف شوند
        db.session.delete(book)
        db.session.commit()
        os.remove(f"static/books/{book.id}.jpg")
        flash('book_del_success')
    return redirect(url_for("admin.books"))