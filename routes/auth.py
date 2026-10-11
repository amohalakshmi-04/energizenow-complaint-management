from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from models.user import User


# Create Authentication Blueprint
auth_bp = Blueprint("auth", __name__)


# =========================
# LOGIN
# =========================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            flash(
                f"Welcome back, {user.name}!",
                "success"
            )

            # -------------------------
            # ROLE-BASED REDIRECTION
            # -------------------------

            if user.role == "admin":

                return redirect(
                    url_for("dashboard.admin_dashboard")
                )

            elif user.role == "staff":

                return redirect(
                    url_for("dashboard.staff_dashboard")
                )

            elif user.role == "customer":

                return redirect(
                    url_for("dashboard.customer_dashboard")
                )

            else:

                return redirect(
                    url_for("dashboard.dashboard")
                )

        else:

            flash(
                "Invalid email or password.",
                "danger"
            )

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )