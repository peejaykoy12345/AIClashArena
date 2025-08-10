from flask import Blueprint, render_template
from AIClashArena.forms import TopicForm

general_bp = Blueprint('general', __name__)

@general_bp.route("/")
@general_bp.route("/home")
def home():
    form = TopicForm()
    return render_template("home.html", form=form)
