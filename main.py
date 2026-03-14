from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig

from pedidos.routes import pedidos_bp
from clientes.routes import clientes_bp
from ventas.routes import ventas_bp

from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(pedidos_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(ventas_bp)

csrf = CSRFProtect()

db.init_app(app)


@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True)