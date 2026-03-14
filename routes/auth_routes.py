from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from models.user import UserModel


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("products.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not email or not senha:
            flash("Preencha email e senha.", "error")
            return render_template("login.html")

        user_model = UserModel(current_app.config["DATABASE_URL"])
        user = user_model.authenticate(email=email, password=senha)

        if not user:
            flash("Credenciais invalidas.", "error")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["user_nome"] = user["nome"]
        session["perfil"] = user["perfil"]

        flash("Login realizado com sucesso.", "success")
        return redirect(url_for("products.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sessao encerrada.", "success")
    return redirect(url_for("auth.login"))
