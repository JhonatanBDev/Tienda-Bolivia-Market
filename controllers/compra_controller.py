from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from models.compra_model import Compra
from models.producto_model import Producto
from database import db
from datetime import datetime

compra_blueprint = Blueprint("compra", __name__)

@compra_blueprint.route("/compras")
@login_required
def ver_compras():
    compras = Compra.query.filter_by(usuario_id=current_user.id).all()
    return render_template("compras.html", compras=compras)

@compra_blueprint.route("/compras/registrar", methods=["GET", "POST"])
@login_required
def registrar_compra():
    if request.method == "POST":
        nueva = Compra(
            usuario_id=current_user.id,
            producto_id=request.form["producto_id"],
            cantidad=request.form["cantidad"],
            fecha=datetime.now(),
            pagado=bool(int(request.form.get("pagado")))
        )
        db.session.add(nueva)
        db.session.commit()
        flash("Compra registrada correctamente.")
        return redirect(url_for("compra.ver_compras"))
    
    productos = Producto.query.all()
    return render_template("registrar_compra.html", productos=productos)

@compra_blueprint.route("/compras/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_compra(id):
    compra = Compra.query.get_or_404(id)
    if compra.usuario_id != current_user.id:
        flash("No tienes permiso para eliminar esta compra.")
        return redirect(url_for("compra.ver_compras"))

    db.session.delete(compra)
    db.session.commit()
    flash("Compra eliminada.")
    return redirect(url_for("compra.ver_compras"))