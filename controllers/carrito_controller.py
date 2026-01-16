# routes/carrito_routes.py
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from models.carrito_model import Carrito
from models.producto_model import Producto
from models.detalle_compra_model import DetalleCompra
from models.compra_model import Compra
from database import db

carrito_blueprint = Blueprint("carrito", __name__)

@carrito_blueprint.route("/carrito/agregar/<int:producto_id>")
@login_required
def agregar_al_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    existente = Carrito.query.filter_by(usuario_id=current_user.id, producto_id=producto_id).first()

    if existente:
        existente.cantidad += 1
    else:
        nuevo = Carrito(usuario_id=current_user.id, producto_id=producto_id, cantidad=1)
        db.session.add(nuevo)
    
    db.session.commit()
    flash("Producto agregado al carrito.")
    return redirect(url_for("productos.lista_productos"))


@carrito_blueprint.route("/carrito")
@login_required
def ver_carrito():
    items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    return render_template("/compras/carrito.html", items=items)

@carrito_blueprint.route("/carrito/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_del_carrito(id):
    item = Carrito.query.get_or_404(id)
    if item.usuario_id != current_user.id:
        flash("No puedes eliminar este producto.")
        return redirect(url_for("carrito.ver_carrito"))
    
    db.session.delete(item)
    db.session.commit()
    flash("Producto eliminado del carrito.")
    return redirect(url_for("carrito.ver_carrito"))


@carrito_blueprint.route("/carrito/comprar", methods=["POST"])
@login_required
def comprar_carrito():
    carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()

    if not carrito_items:
        flash("Tu carrito está vacío.")
        return redirect(url_for("carrito.ver_carrito"))

    for item in carrito_items:
        # Crear una compra por producto (puedes agrupar si quieres)
        compra = Compra(
            usuario_id=current_user.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            pagado=True  # o False, si luego se paga
        )
        db.session.add(compra)
        db.session.flush()  # para obtener compra.id

        detalle = DetalleCompra(
            compra_id=compra.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        db.session.add(detalle)

    # Vaciar carrito
    Carrito.query.filter_by(usuario_id=current_user.id).delete()

    db.session.commit()
    flash("¡Compra realizada con éxito!")
    return redirect(url_for("productos.lista_productos"))


@carrito_blueprint.route("/carrito/comprar/<int:id>", methods=["POST"])
@login_required
def comprar_item(id):
    item = Carrito.query.get_or_404(id)

    # Verifica que el item pertenezca al usuario actual
    if item.usuario_id != current_user.id:
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("carrito.ver_carrito"))

    # Crear la compra
    compra = Compra(
        usuario_id=current_user.id,
        producto_id=item.producto_id,
        cantidad=item.cantidad,
        pagado=True
    )
    db.session.add(compra)
    db.session.flush()  # Para tener compra.id disponible

    # Crear detalle
    detalle = DetalleCompra(
        compra_id=compra.id,
        producto_id=item.producto_id,
        cantidad=item.cantidad,
        precio_unitario=item.producto.precio
    )
    db.session.add(detalle)

    # Eliminar solo este ítem del carrito
    db.session.delete(item)

    db.session.commit()
    flash("Producto comprado exitosamente.")
    return redirect(url_for("carrito.ver_carrito"))


@carrito_blueprint.route("/carrito/iniciar_pago", methods=["POST"])
@login_required
def iniciar_pago():
    carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()

    if not carrito_items:
        flash("Tu carrito está vacío.")
        return redirect(url_for("carrito.ver_carrito"))

    compras = []

    for item in carrito_items:
        compra = Compra(
            usuario_id=current_user.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            pagado=False  # aún no ha pagado
        )
        db.session.add(compra)
        db.session.flush()

        detalle = DetalleCompra(
            compra_id=compra.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        db.session.add(detalle)
        compras.append(compra)

    db.session.commit()

    # Mostrar página con botón PayPal y lista de compras pendientes
    return render_template("/compras/pago_paypal.html", compras=compras)

@carrito_blueprint.route("/carrito/confirmar_pago")
@login_required
def confirmar_pago():
    compras_no_pagadas = Compra.query.filter_by(usuario_id=current_user.id, pagado=False).all()

    for compra in compras_no_pagadas:
        compra.pagado = True

    # Vacía el carrito
    Carrito.query.filter_by(usuario_id=current_user.id).delete()
    db.session.commit()

    flash("¡Pago confirmado con PayPal y compra registrada!")
    return redirect(url_for("productos.lista_productos"))

@carrito_blueprint.route("/carrito/pago_individual/<int:id>", methods=["GET"])
@login_required
def pago_individual(id):
    item = Carrito.query.get_or_404(id)
    if item.usuario_id != current_user.id:
        flash("No tienes permiso para ver este ítem.")
        return redirect(url_for("carrito.ver_carrito"))
    return render_template("/compras/pago_individual.html", item=item)

@carrito_blueprint.route("/carrito/confirmar_individual/<int:id>")
@login_required
def confirmar_pago_individual(id):
    item = Carrito.query.get_or_404(id)

    if item.usuario_id != current_user.id:
        flash("No autorizado.")
        return redirect(url_for("carrito.ver_carrito"))

    compra = Compra(
        usuario_id=current_user.id,
        producto_id=item.producto_id,
        cantidad=item.cantidad,
        pagado=True
    )
    db.session.add(compra)
    db.session.flush()

    detalle = DetalleCompra(
        compra_id=compra.id,
        producto_id=item.producto_id,
        cantidad=item.cantidad,
        precio_unitario=item.producto.precio
    )
    db.session.add(detalle)

    db.session.delete(item)
    db.session.commit()

    flash("Compra realizada exitosamente con PayPal.")
    return redirect(url_for("productos.lista_productos"))
