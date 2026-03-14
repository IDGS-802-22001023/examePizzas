from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

# Formulario para nuevo pedido
class PedidoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    direccion = StringField("Dirección", validators=[DataRequired()])
    telefono = StringField("Teléfono", validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired()])

# Formulario para filtrar ventas por día
class DiasForm(FlaskForm):
    dias = SelectMultipleField(
        "Selecciona los días",
        choices=[
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miércoles", "Miércoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
            ("Sábado", "Sábado"),
            ("Domingo", "Domingo"),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Filtrar")

# Formulario para filtrar ventas por mes
class MesesForm(FlaskForm):
    meses = SelectMultipleField(
        "Selecciona los meses",
        choices=[
            ("Enero", "Enero"),
            ("Febrero", "Febrero"),
            ("Marzo", "Marzo"),
            ("Abril", "Abril"),
            ("Mayo", "Mayo"),
            ("Junio", "Junio"),
            ("Julio", "Julio"),
            ("Agosto", "Agosto"),
            ("Septiembre", "Septiembre"),
            ("Octubre", "Octubre"),
            ("Noviembre", "Noviembre"),
            ("Diciembre", "Diciembre"),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Filtrar")