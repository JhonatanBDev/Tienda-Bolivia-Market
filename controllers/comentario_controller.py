from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from models.comentario_model import Comentario
from database import db

comentario_blueprint = Blueprint("comentarios", __name__)

@comentario_blueprint.route("/comentario/agregar/<int:producto_id>", methods=["POST"])
@login_required
def agregar_comentario(producto_id):
    contenido = request.form["contenido"]
    comentario = Comentario(
        contenido=contenido,
        usuario_id=current_user.id,
        producto_id=producto_id
    )
    db.session.add(comentario)
    db.session.commit()
    flash("Comentario agregado.")
    return redirect(url_for("productos.detalle_producto", id=producto_id))

@comentario_blueprint.route("/comentario/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_comentario(id):
    comentario = Comentario.query.get_or_404(id)
    if comentario.usuario_id != current_user.id:
        flash("No puedes eliminar este comentario.")
        return redirect(url_for("productos.detalle_producto", id=comentario.producto_id))

    db.session.delete(comentario)
    db.session.commit()
    flash("Comentario eliminado.")
    return redirect(url_for("productos.detalle_producto", id=comentario.producto_id))

@comentario_blueprint.route("/comentario/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_comentario(id):
    comentario = Comentario.query.get_or_404(id)
    if comentario.usuario_id != current_user.id:
        flash("No puedes editar este comentario.")
        return redirect(url_for("productos.detalle_producto", id=comentario.producto_id))

    if request.method == "POST":
        comentario.contenido = request.form["contenido"]
        db.session.commit()
        flash("Comentario actualizado.")
        return redirect(url_for("productos.detalle_producto", id=comentario.producto_id))

    return render_template("/calificadoras/editar_comentario.html", comentario=comentario)
