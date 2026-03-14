from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Clientes(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))

    pedidos = db.relationship(
        "Pedidos",
        back_populates="cliente",
        cascade="all, delete"
    )


class Pizzas(db.Model):
    __tablename__ = "pizzas"

    id_pizza = db.Column(db.Integer, primary_key=True)
    tamano = db.Column(db.String(20))
    ingredientes = db.Column(db.String(200))
    precio = db.Column(db.Numeric(8,2))

    detalles = db.relationship(
        "DetallePedido",
        back_populates="pizza"
    )


class Pedidos(db.Model):
    __tablename__ = "pedidos"

    id_pedido = db.Column(db.Integer, primary_key=True)

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),
        nullable=False
    )

    fecha = db.Column(
        db.Date,
        default=datetime.date.today
    )

    total = db.Column(db.Numeric(10,2))

    cliente = db.relationship(
        "Clientes",
        back_populates="pedidos"
    )

    detalles = db.relationship(
        "DetallePedido",
        back_populates="pedido",
        cascade="all, delete"
    )


class DetallePedido(db.Model):
    __tablename__ = "detalle_pedido"

    id_detalle = db.Column(db.Integer, primary_key=True)

    id_pedido = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id_pedido"),
        nullable=False
    )

    id_pizza = db.Column(
        db.Integer,
        db.ForeignKey("pizzas.id_pizza"),
        nullable=False
    )

    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10,2))

    pedido = db.relationship(
        "Pedidos",
        back_populates="detalles"
    )

    pizza = db.relationship(
        "Pizzas",
        back_populates="detalles"
    )


# SEGUNDA TABLA (nombre de clase diferente)
class DetallePedidoExtra(db.Model):
    __tablename__ = "detallepedido"

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id_pedido"))
    id_pizza = db.Column(db.Integer, db.ForeignKey("pizzas.id_pizza"))
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Float)

    pedido = db.relationship("Pedidos")
    pizza = db.relationship("Pizzas")