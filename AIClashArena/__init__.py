from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ILOVESKIBIDITOILET'

from AIClashArena.routes import general_bp
from AIClashArena.api_routes import api_bp

app.register_blueprint(general_bp)
app.register_blueprint(api_bp, url_prefix="/api")