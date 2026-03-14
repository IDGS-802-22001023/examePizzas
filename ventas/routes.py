from flask import Blueprint, render_template, request
from models import Pedidos
from forms import DiasForm, MesesForm

ventas_bp = Blueprint(
    "ventas",
    __name__,
    url_prefix="/ventas"
)

@ventas_bp.route("/", methods=["GET", "POST"])
def ventas():
    dias_form = DiasForm(prefix="dias")
    meses_form = MesesForm(prefix="meses")
    pedidos = []

    dias_traducidos = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    meses_dict = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    todos_pedidos = Pedidos.query.all()

    # valores por defecto
    dias_seleccionados = list(dias_traducidos.values())
    meses_seleccionados = list(meses_dict.values())

    if request.method == "POST":
        dias_seleccionados = request.form.getlist("dias") or dias_seleccionados
        meses_seleccionados = request.form.getlist("meses") or meses_seleccionados

    # filtrar pedidos por día y mes
    for pedido in todos_pedidos:
        dia_nombre = dias_traducidos[pedido.fecha.strftime("%A")]
        mes_nombre = meses_dict[pedido.fecha.month]
        if dia_nombre in dias_seleccionados and mes_nombre in meses_seleccionados:
            pedidos.append(pedido)

    # actualizar formularios con los seleccionados
    dias_form.dias.data = dias_seleccionados
    meses_form.meses.data = meses_seleccionados

    total = sum(p.total for p in pedidos) if pedidos else 0

    return render_template(
        "ventas.html",
        pedidos=pedidos,
        dias_form=dias_form,
        meses_form=meses_form,
        total=total
    )