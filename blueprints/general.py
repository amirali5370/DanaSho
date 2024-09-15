from flask import Blueprint, render_template
from models.slides import Slide

app = Blueprint("general" , __name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404page.html"), 404

@app.route("/about")
def about():
    return "about us"
