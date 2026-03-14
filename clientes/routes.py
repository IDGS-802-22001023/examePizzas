from flask import Blueprint, render_template
from models import db, Clientes

clientes_bp = Blueprint(
    "clientes",
    __name__,
    url_prefix="/clientes"
)

@clientes_bp.route("/")
def lista_clientes():

    clientes = Clientes.query.all()

    return render_template(
        "clientes_pedidos.html",
        clientes=clientes
    )