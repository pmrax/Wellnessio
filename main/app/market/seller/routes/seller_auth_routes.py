from flask import Blueprint, render_template

seller_auth_bp = Blueprint("seller_auth", __name__)

@seller_auth_bp.route("/seller")
def seller():
    return render_template("market/seller/seller.html")

@seller_auth_bp.route("/seller/register", methods=["GET"])
def register():
    return render_template("market/seller/seller_register.html")


