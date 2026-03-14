from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from models.user import UserModel
from routes import admin_required


user_bp = Blueprint("users", __name__, url_prefix="/usuarios")


@user_bp.route("/")
@admin_required
def list_users():
    user_model = UserModel(current_app.config["DATABASE_URL"])
    users = user_model.list_users()
    return render_template("users/list.html", users=users)


@user_bp.route("/novo", methods=["GET", "POST"])
@admin_required
def create_user():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        perfil = request.form.get("perfil", "comum").strip()

        if not nome or not email or not senha:
            flash("Nome, email e senha sao obrigatorios.", "error")
            return render_template("users/form.html")

        user_model = UserModel(current_app.config["DATABASE_URL"])
        ok, message = user_model.create_user(
            nome=nome,
            email=email,
            senha=senha,
            perfil=perfil,
            criado_por=session["user_id"],
        )
        flash(message, "success" if ok else "error")
        if ok:
            return redirect(url_for("users.list_users"))

    return render_template("users/form.html")
