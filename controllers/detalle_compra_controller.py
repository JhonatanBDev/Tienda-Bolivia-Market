# routes/detalle_compra_routes.py
from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from models.detalle_compra_model import DetalleCompra
from models.producto_model import Producto
from models.compra_model import Compra
from database import db

detalle_compra_blueprint = Blueprint("detalle_compra", __name__)

@detalle_compra_blueprint.route("/detalle-compra/<int:compra_id>")
@login_required
def ver_detalle_compra(compra_id):
    detalles = DetalleCompra.query.filter_by(compra_id=compra_id).all()
    return render_template("/compras/detalle_compra.html", detalles=detalles, compra_id=compra_id)

@detalle_compra_blueprint.route("/detalle-compra/agregar/<int:producto_id>/<int:compra_id>")
@login_required
def agregar_detalle_compra(producto_id, compra_id):
    producto = Producto.query.get_or_404(producto_id)
    Compra.query.get_or_404(compra_id)

    existente = DetalleCompra.query.filter_by(compra_id=compra_id, producto_id=producto_id).first()

    if existente:
        existente.cantidad += 1
    else:
        nuevo = DetalleCompra(
            compra_id=compra_id,
            producto_id=producto_id,
            cantidad=1,
            precio_unitario=producto.precio  # Asegúrate que el modelo Producto tiene 'precio'
        )
        db.session.add(nuevo)

    db.session.commit()
    flash("Producto agregado al detalle de compra.")
    return redirect(url_for("detalle_compra.ver_detalle_compra", compra_id=compra_id))

@detalle_compra_blueprint.route("/detalle-compra/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_detalle_compra(id):
    detalle = DetalleCompra.query.get_or_404(id)
    compra_id = detalle.compra_id

    db.session.delete(detalle)
    db.session.commit()
    flash("Producto eliminado del detalle de compra.")
    return redirect(url_for("detalle_compra.ver_detalle_compra", compra_id=compra_id))