from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.mensaje_model import Mensaje
from models.usuario_model import Usuario
from database import db
from datetime import datetime

mensaje_blueprint = Blueprint("mensaje", __name__)

@mensaje_blueprint.route("/mensajes")
@login_required
def bandeja_entrada():
    mensajes = Mensaje.query.filter_by(receptor_id=current_user.id).order_by(Mensaje.fecha_envio.desc()).all()
    return render_template("/usuarios/enviar_mensaje.html", mensajes=mensajes)

@mensaje_blueprint.route("/mensajes/enviar", methods=["GET", "POST"])
@login_required
def enviar_mensaje():
    if request.method == "POST":
        nombre_receptor = request.form["receptor"]
        receptor = Usuario.query.filter_by(username=nombre_receptor).first()

        if not receptor:
            flash("Usuario no encontrado.")
            return redirect(url_for("mensaje.enviar_mensaje"))

        nuevo = Mensaje(
            emisor_id=current_user.id,
            receptor_id=receptor.id,
            contenido=request.form["contenido"],
            fecha_envio=datetime.now()
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Mensaje enviado correctamente.")
        return redirect(url_for("mensaje.bandeja_entrada"))

    return render_template("/usuarios/enviar_mensaje.html")
    
@mensaje_blueprint.route("/mensajes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_mensaje(id):
    mensaje = Mensaje.query.get_or_404(id)
    if mensaje.receptor_id != current_user.id and mensaje.emisor_id != current_user.id:
        flash("No tienes permiso para eliminar este mensaje.")
        return redirect(url_for("mensaje.bandeja_entrada"))

    db.session.delete(mensaje)
    db.session.commit()
    flash("Mensaje eliminado.")
    return redirect(url_for("mensaje.bandeja_entrada"))