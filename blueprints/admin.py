from flask import Blueprint, jsonify, render_template, request, session, redirect, abort, flash, url_for
import os
import config
from models.user import User
from models.slides import Slide
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


##############################   STUDENT   ###############################
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

























# ---------------------------------OLD CODE---------------------------------------

@app.route("/admin/dashboard/del-students/<id>", methods = ["GET", "POST"])
def delete_user(id):
    status = request.args.get("status")
    if status == "true":
        students = User.query.filter(User.id == id).first_or_404()
        # TODO : نتایج امحاناتش حذف شود
        db.session.delete(students)
        db.session.commit()
        flash('del success')
    return redirect(url_for("admin.classes"))


##############################   SETTING   ###############################
@app.route("/admin/dashboard/slider", methods = ["GET","POST"])
def slider_setting():
    slides = Slide.query.all()
    if request.method == "POST":
        head = request.form.get("head", None)
        text = request.form.get("text", None)
        active = request.form.get("active", None)
        if active == "active":
            activate = 1
        else:
            activate = 0
        mode = request.form.get("mode", None)
        if mode=="add":
            file = request.files.get("slide", None)

            s = Slide(head=head,text=text,active=activate)
            db.session.add(s)
            db.session.commit()
            file.save(f"static/slides/{s.id}.jpg")

            flash('add success')
            return redirect(url_for('admin.slider_setting'))

        else:
            s = Slide.query.filter(Slide.id==int(mode)).first_or_404()
            s.head = head
            s.text = text
            if active == "active":
                s.active = True
            else:
                s.active = False

            db.session.commit()
            flash('edit success')
            return redirect(url_for('admin.slider_setting'))
            
    else:
        return render_template("admin/slider.html", slides=slides)


@app.route("/admin/dashboard/slider/<id>", methods = ["GET","POST"])
def slide_delete(id):
    status = request.args.get("status")
    if status == "true":
        slide = Slide.query.filter(Slide.id == id).first_or_404()
        db.session.delete(slide)
        db.session.commit()
        os.remove(f"static/slides/{slide.id}.jpg")

        flash('del success')
    return redirect(url_for("admin.teachers"))
