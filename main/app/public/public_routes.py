from flask import Blueprint, render_template

public_bp = Blueprint("public", __name__)

@public_bp.route("/about", methods=["GET"])
def about():
    return render_template("public/who_we_are.html")

@public_bp.route("/service")
def service():
    return render_template("public/our_service.html")

@public_bp.route("/community")
def community():
    return render_template("public/join_community.html")

@public_bp.route("/goal")
def goal():
    return render_template("public/goal_track.html")

@public_bp.route("/game")
def game():
    return render_template("public/wellness_games.html")
