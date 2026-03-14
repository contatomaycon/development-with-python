from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from models.movement import MovementModel
from models.product import ProductModel
from routes import admin_required, login_required


product_bp = Blueprint("products", __name__, url_prefix="/produtos")


@product_bp.route("/dashboard")
@login_required
def dashboard():
    product_model = ProductModel(current_app.config["DATABASE_URL"])
    low_stock = product_model.list_low_stock()
    products = product_model.list_products()
    return render_template(
        "dashboard.html",
        total_products=len(products),
        low_stock=low_stock,
    )


@product_bp.route("/")
@login_required
def list_products():
    product_model = ProductModel(current_app.config["DATABASE_URL"])
    products = product_model.list_products()
    return render_template("products/list.html", products=products)


@product_bp.route("/novo", methods=["GET", "POST"])
@admin_required
def create_product():
    if request.method == "POST":
        data = {
            "nome": request.form.get("nome", "").strip(),
            "descricao": request.form.get("descricao", "").strip(),
            "preco": request.form.get("preco", "").strip(),
            "quantidade": request.form.get("quantidade", "").strip(),
            "quantidade_minima": request.form.get("quantidade_minima", "").strip(),
            "categoria": request.form.get("categoria", "").strip(),
        }
        product_model = ProductModel(current_app.config["DATABASE_URL"])
        ok, message = product_model.create_product(data, session["user_id"])
        flash(message, "success" if ok else "error")
        if ok:
            return redirect(url_for("products.list_products"))
        return render_template("products/form.html", form_data=data, form_mode="create")

    return render_template("products/form.html", form_data={}, form_mode="create")


@product_bp.route("/<int:product_id>/editar", methods=["GET", "POST"])
@admin_required
def edit_product(product_id: int):
    product_model = ProductModel(current_app.config["DATABASE_URL"])
    product = product_model.get_product(product_id)
    if not product:
        flash("Produto nao encontrado.", "error")
        return redirect(url_for("products.list_products"))

    if request.method == "POST":
        data = {
            "nome": request.form.get("nome", "").strip(),
            "descricao": request.form.get("descricao", "").strip(),
            "preco": request.form.get("preco", "").strip(),
            "quantidade": request.form.get("quantidade", "").strip(),
            "quantidade_minima": request.form.get("quantidade_minima", "").strip(),
            "categoria": request.form.get("categoria", "").strip(),
        }
        ok, message = product_model.update_product(product_id, data, session["user_id"])
        flash(message, "success" if ok else "error")
        if ok:
            return redirect(url_for("products.list_products"))
        return render_template("products/form.html", form_data=data, form_mode="edit", product_id=product_id)

    return render_template("products/form.html", form_data=product, form_mode="edit", product_id=product_id)


@product_bp.route("/<int:product_id>/movimentar", methods=["POST"])
@admin_required
def register_movement(product_id: int):
    tipo = request.form.get("tipo", "").strip()
    quantidade_raw = request.form.get("quantidade", "").strip()
    motivo = request.form.get("motivo", "").strip()

    try:
        quantidade = int(quantidade_raw)
    except ValueError:
        flash("Quantidade deve ser numero inteiro.", "error")
        return redirect(url_for("products.list_products"))

    movement_model = MovementModel(current_app.config["DATABASE_URL"])
    ok, message = movement_model.register_movement(
        product_id=product_id,
        tipo=tipo,
        quantidade=quantidade,
        usuario_id=session["user_id"],
        motivo=motivo,
    )
    flash(message, "success" if ok else "error")
    return redirect(url_for("products.list_products"))


@product_bp.route("/movimentacoes")
@admin_required
def list_movements():
    movement_model = MovementModel(current_app.config["DATABASE_URL"])
    movements = movement_model.list_movements()
    return render_template("products/movements.html", movements=movements)
