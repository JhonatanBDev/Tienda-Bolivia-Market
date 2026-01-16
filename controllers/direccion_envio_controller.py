# routes/direccion_envio_routes.py
from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from database import db
from models.direccion_model import DireccionEnvio

direccion_envio_blueprint = Blueprint("direccion_envio", __name__)

@direccion_envio_blueprint.route("/direccion-envio")
@login_required
def ver_direccion_envio():
    direccion = DireccionEnvio.query.filter_by(usuario_id=current_user.id).first()
    return render_template("/compras/direccion_envio.html", direccion=direccion)

@direccion_envio_blueprint.route("/direccion-envio/guardar", methods=["POST"])
@login_required
def guardar_direccion_envio():
    direccion = DireccionEnvio.query.filter_by(usuario_id=current_user.id).first()

    if direccion:
        # Actualiza si ya existe
        direccion.direccion = request.form["direccion"]
        direccion.ciudad = request.form["ciudad"]
        direccion.departamento = request.form["departamento"]
        direccion.pais = request.form["pais"]
        direccion.telefono = request.form["telefono"]
    else:
        # Crea nueva dirección
        nueva = DireccionEnvio(
            usuario_id=current_user.id,
            direccion=request.form["direccion"],
            ciudad=request.form["ciudad"],
            departamento=request.form["departamento"],
            pais=request.form["pais"],
            telefono=request.form["telefono"]
        )
        db.session.add(nueva)

    db.session.commit()
    flash("Dirección de envío guardada exitosamente.")
    return redirect(url_for("direccion_envio.ver_direccion_envio"))

@direccion_envio_blueprint.route("/direccion-envio/eliminar", methods=["POST"])
@login_required
def eliminar_direccion_envio():
    direccion = DireccionEnvio.query.filter_by(usuario_id=current_user.id).first()
    if direccion:
        db.session.delete(direccion)
        db.session.commit()
        flash("Dirección eliminada.")
    else:
        flash("No se encontró ninguna dirección para eliminar.")
    return redirect(url_for("direccion_envio.ver_direccion_envio"))