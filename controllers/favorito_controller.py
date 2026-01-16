from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from models.favorito_model import Favorito

from database import db

favorito_blueprint = Blueprint("favoritos", __name__)

@favorito_blueprint.route("/favorito/agregar", methods=["POST"])
@login_required
def agregar_favorito():
    producto_id = int(request.form["producto_id"])

    favorito_existente = Favorito.query.filter_by(
        usuario_id=current_user.id,
        producto_id=producto_id
    ).first()

    if favorito_existente:
        flash("Este producto ya está en tus favoritos.")
    else:
        nuevo_favorito = Favorito(
            usuario_id=current_user.id,
            producto_id=producto_id
        )
        db.session.add(nuevo_favorito)
        db.session.commit()
        flash("Producto agregado a favoritos.")

    return redirect(url_for("productos.lista_productos"))

@favorito_blueprint.route("/favoritos")
@login_required
def ver_favoritos():
    favoritos = Favorito.query.filter_by(usuario_id=current_user.id).all()
    return render_template("/calificadoras/favoritos.html", favoritos=favoritos)

@favorito_blueprint.route("/favorito/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_favorito(id):
    favorito = Favorito.query.get_or_404(id)

    if favorito.usuario_id != current_user.id:
        flash("No puedes eliminar este favorito.")
        return redirect(url_for("favoritos.ver_favoritos"))

    db.session.delete(favorito)
    db.session.commit()
    flash("Producto eliminado de favoritos.")
    return redirect(url_for("favoritos.ver_favoritos"))