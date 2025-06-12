from flask import Blueprint, render_template

market_bp = Blueprint("market", __name__)

@market_bp.route("/market", methods=["GET"])
def market():
    return render_template("market/market.html")


