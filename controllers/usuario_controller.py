from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from models.usuario_model import Usuario
from database import db
from models.compra_model import Compra

usuario_blueprint = Blueprint("usuarios", __name__)

#lista usuarios
@usuario_blueprint.route("/usuarios")
def lista_usuarios():
    usuarios = Usuario.query.all()
    return render_template("/usuarios/lista_usuarios.html", usuarios=usuarios,usuario=current_user)

#detalle 
@usuario_blueprint.route("/usuario/<int:id>")
def detalle_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("/usuarios/detalle_usuario.html", usuario=usuario)


#editar 
@usuario_blueprint.route("/usuario/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        usuario.username = request.form["username"]
        usuario.email = request.form["email"]
        usuario.password = generate_password_hash(request.form['password'])
        usuario.rol = request.form["rol"]
        db.session.commit()
        flash("Usuario actualizado.")
        return redirect(url_for("usuarios.lista_usuarios"))
    return render_template("/usuarios/editar_usuario.html", usuario=usuario)


@usuario_blueprint.route("/usuario/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.id != current_user.id and current_user.rol != 'admin':
        flash("No tienes permiso para eliminar este usuario.")
        return redirect(url_for("usuarios.lista_usuarios"))

    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario y productos asociados eliminados.")
    return redirect(url_for("usuarios.lista_usuarios"))





@usuario_blueprint.route("/usuario/<int:id>/compras")
@login_required
def mis_compras(id):
    if current_user.id != id:
        flash("No puedes ver las compras de otro usuario.")
        return redirect(url_for('productos.lista_productos'))

    compras = Compra.query.filter_by(usuario_id=id).order_by(Compra.fecha.desc()).all()
    return render_template("/compras/mis_compras.html", compras=compras)

@usuario_blueprint.route("/admin/marcar_pago/<int:id>/<estado>", methods=["POST"])
@login_required
def marcar_pago(id, estado):
    if current_user.rol != "admin":
        flash("No tienes permisos para realizar esta acción.")
        return redirect(url_for("productos.lista_productos"))

    compra = Compra.query.get_or_404(id)
    compra.pagado = True if estado == "si" else False
    db.session.commit()

    flash(f"Compra marcada como {'pagada' if compra.pagado else 'no pagada'}.")
    return redirect(url_for("usuarios.mis_compras", id=compra.usuario_id))
