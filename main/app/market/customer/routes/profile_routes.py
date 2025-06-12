from flask import Blueprint, render_template
from flask_login import login_required

market_profile_bp = Blueprint("market_profile", __name__)

@market_profile_bp.route("/mprofile", methods=["GET"])
@login_required
def market_profile():

    return render_template("market/customer/profile.html")


