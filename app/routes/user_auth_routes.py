from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from app.models.user_auth_model import Customer
from app import auth_mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def index():
    """Render the index page with user details if logged in."""
    user_name = session.get("user_name")
    return render_template("index.html", user_name=user_name)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        mobile_no = request.form.get("mobile_no")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        result = Customer.register(username, email, mobile_no, password, confirm_password)
        
        if "error" in result:
            flash(result["error"], "danger")
            return redirect(url_for("auth.register"))

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        identifier = request.form.get("identifier")  # Email or mobile
        password = request.form.get("password")

        result = Customer.login(identifier, password)

        if "error" in result:
            flash(result["error"], "danger")
            return redirect(url_for("auth.login"))

        # Log in user and store session data
        user = result["customer"]
        session["user_name"] = user.username  # Store username in session
        
        flash("Login successful!", "success")
        return redirect(url_for("auth.index"))

    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    """Handle user logout."""
    session.pop("user_name", None)  # Remove user session
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.index"))
