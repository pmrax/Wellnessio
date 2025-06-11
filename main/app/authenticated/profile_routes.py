from flask import Blueprint, render_template
from flask_login import login_required

profile_bp = Blueprint("profile", __name__)

@login_required
@profile_bp.route("/profile", methods=["GET"])
def profile():
    return render_template("authed/profile.html")



