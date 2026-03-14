from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Clientes, Pedidos, DetallePedido, Pizzas
from datetime import date, datetime
from forms import PedidoForm

pedidos_bp = Blueprint(
    "pedidos",
    __name__,
    url_prefix="/pedidos"
)

# carrito en session
def obtener_carrito():
    if "carrito" not in session:
        session["carrito"] = []
    return session["carrito"]

@pedidos_bp.route("/detalle/<int:id>")
def detalle_pedido(id):

    pedido = Pedidos.query.get_or_404(id)

    detalles = db.session.query(DetallePedido, Pizzas).join(
        Pizzas, Pizzas.id_pizza == DetallePedido.id_pizza
    ).filter(
        DetallePedido.id_pedido == id
    ).all()

    return render_template(
        "detalle_pedido.html",
        pedido=pedido,
        detalles=detalles
    )

@pedidos_bp.route("/", methods=["GET", "POST"])
def nuevo_pedido():

    form = PedidoForm()
    carrito = obtener_carrito()

    if request.method == "POST":

        accion = request.form.get("accion")

        # guardar datos cliente y fecha en session
        session["nombre"] = request.form.get("nombre")
        session["direccion"] = request.form.get("direccion")
        session["telefono"] = request.form.get("telefono")
        session["fecha"] = request.form.get("fecha")

        # -------- AGREGAR PIZZA --------
        if accion == "agregar":

            tamano = request.form.get("tamano")
            ingredientes = request.form.getlist("ingredientes")
            cantidad = request.form.get("cantidad")

            if not tamano or not cantidad:
                return redirect(url_for("pedidos.nuevo_pedido"))

            cantidad = int(cantidad)
            ingredientes_str = ", ".join(ingredientes)

            precios = {"Chica": 40, "Mediana": 80, "Grande": 120}
            precio_base = precios[tamano]
            precio_ingredientes = len(ingredientes) * 10
            precio_total = precio_base + precio_ingredientes
            subtotal = precio_total * cantidad

            item = {
                "tamano": tamano,
                "ingredientes": ingredientes_str,
                "cantidad": cantidad,
                "precio": precio_total,
                "subtotal": subtotal
            }

            carrito.append(item)
            session["carrito"] = carrito

        # -------- QUITAR ÚLTIMA PIZZA --------
        elif accion == "quitar":
            if carrito:
                carrito.pop()
                session["carrito"] = carrito

        # -------- ELIMINAR PIZZA POR FILA --------
        elif accion == "eliminar":
            indice = request.args.get("indice", type=int)
            if indice is not None and 0 <= indice < len(carrito):
                carrito.pop(indice)
                session["carrito"] = carrito

        # -------- TERMINAR PEDIDO --------
        elif accion == "terminar":

            if not carrito:
                return redirect(url_for("pedidos.nuevo_pedido"))

            nombre = session.get("nombre")
            direccion = session.get("direccion")
            telefono = session.get("telefono")
            fecha_str = session.get("fecha")

            if not nombre or not direccion or not telefono or not fecha_str:
                return redirect(url_for("pedidos.nuevo_pedido"))

            total = sum(item["subtotal"] for item in carrito)
            fecha_pedido = datetime.strptime(fecha_str, "%Y-%m-%d").date()

            try:
                # cliente
                cliente = Clientes(
                    nombre=nombre,
                    direccion=direccion,
                    telefono=telefono
                )
                db.session.add(cliente)
                db.session.flush()

                # pedido
                pedido = Pedidos(
                    id_cliente=cliente.id_cliente,
                    fecha=fecha_pedido,
                    total=total
                )
                db.session.add(pedido)
                db.session.flush()

                # detalle
                for item in carrito:
                    pizza = Pizzas(
                        tamano=item["tamano"],
                        ingredientes=item["ingredientes"],
                        precio=item["precio"]
                    )
                    db.session.add(pizza)
                    db.session.flush()

                    detalle = DetallePedido(
                        id_pedido=pedido.id_pedido,
                        id_pizza=pizza.id_pizza,
                        cantidad=item["cantidad"],
                        subtotal=item["subtotal"]
                    )
                    db.session.add(detalle)

                db.session.commit()

                # limpiar carrito y session solo al finalizar
                session.pop("carrito", None)
                session.pop("nombre", None)
                session.pop("direccion", None)
                session.pop("telefono", None)
                session.pop("fecha", None)

                return redirect(url_for("pedidos.nuevo_pedido"))

            except Exception as e:
                db.session.rollback()
                print("ERROR:", e)

    # al renderizar, pasar fecha para que se mantenga en el formulario
    fecha = session.get("fecha", "")

    total = sum(item["subtotal"] for item in carrito)

    return render_template(
        "pedido.html",
        carrito=carrito,
        total=total,
        form=form,
        fecha=fecha
    )