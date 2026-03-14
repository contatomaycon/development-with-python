from flask import Flask, redirect, url_for

from config import Config
from models.database import init_db
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.user_routes import user_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app.config["DATABASE_URL"])

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)

    @app.route("/")
    def index():
        return redirect(url_for("products.dashboard"))

    @app.errorhandler(403)
    def forbidden(_error):
        from flask import render_template

        return render_template("403.html"), 403

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
