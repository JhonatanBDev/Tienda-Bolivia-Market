# routes/producto_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.producto_model import Producto
from models.categoria_model import Categoria
from models.comentario_model import Comentario

from database import db

producto_blueprint = Blueprint("productos", __name__)

@producto_blueprint.route("/producto/agregar", methods=["GET", "POST"])
@login_required
def agregar_producto():
    categorias = Categoria.query.all()  # <--- Esto debe traer categorías

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        precio = float(request.form["precio"])
        imagen = request.form["imagen"]
        categoria_id = request.form["categoria_id"]

        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            imagen=imagen,
            usuario_id=current_user.id,
            categoria_id=categoria_id
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash("Producto agregado correctamente.")
        return redirect(url_for("productos.lista_productos"))

    return render_template("/productos/agregar_producto.html", categorias=categorias)

@producto_blueprint.route("/home")
def ver_productos():
    productos = Producto.query.all()
    return render_template("index.html", productos=productos)

@producto_blueprint.route("/producto/<int:id>")
def detalle_producto(id):
    producto = Producto.query.get_or_404(id)

    # Asegúrate de importar Comentario y hacer esta consulta
    comentarios = Comentario.query.filter_by(producto_id=id).order_by(Comentario.fecha.desc()).all()

    return render_template("/productos/detalle_producto.html", producto=producto, comentarios=comentarios)

@producto_blueprint.route("/productos")
def lista_productos():
    productos = Producto.query.all()
    return render_template("/productos/lista_productos.html", productos=productos,usuario=current_user)

@producto_blueprint.route("/producto/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    if producto.usuario_id != current_user.id:
        flash("No tienes permiso para eliminar este producto.")
        return redirect(url_for("productos.lista_productos"))

    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado.")
    return redirect(url_for("productos.lista_productos"))

#editar
@producto_blueprint.route("/producto/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    if producto.usuario_id != current_user.id:
        flash("No tienes permiso para editar este producto.")
        return redirect(url_for("productos.lista_productos"))

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.descripcion = request.form["descripcion"]
        producto.precio = float(request.form["precio"])
        producto.imagen = request.form["imagen"]
        db.session.commit()
        flash("Producto actualizado correctamente.")
        return redirect(url_for("productos.lista_productos"))

    return render_template("/productos/editar_producto.html", producto=producto)


