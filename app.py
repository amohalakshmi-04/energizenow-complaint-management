from flask import Flask, render_template
from flask_login import LoginManager

from config import Config
from models import db, User

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.complaints import complaints_bp
from routes.service_requests import service_requests_bp


# =========================
# CREATE FLASK APPLICATION
# =========================

app = Flask(__name__)

app.config.from_object(Config)


# =========================
# DATABASE
# =========================

db.init_app(app)


# =========================
# LOGIN MANAGER
# =========================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# =========================
# REGISTER BLUEPRINTS
# =========================

app.register_blueprint(auth_bp)

app.register_blueprint(dashboard_bp)

app.register_blueprint(complaints_bp)

app.register_blueprint(service_requests_bp)


# =========================
# CREATE DATABASE TABLES
# =========================

with app.app_context():

    db.create_all()


# =========================
# PUBLIC HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(debug=True)