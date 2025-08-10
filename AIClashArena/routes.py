import requests
from flask import Blueprint, render_template
from AIClashArena.forms import TopicForm

general_bp = Blueprint('general', __name__)

@general_bp.route("/")
@general_bp.route("/home")
def home():
    return render_template("home.html")

@general_bp.route("/debate", methods=["POST", "GET"])
def debate():
    form = TopicForm()
    if form.validate_on_submit():
        topic = form.topic.data
        return render_template("debate.html", topic=topic)
    return render_template("topic_selector.html", form=form)

