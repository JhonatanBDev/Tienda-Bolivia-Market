from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.categoria_model import Categoria
from database import db

categoria_blueprint = Blueprint("categorias", __name__)

@categoria_blueprint.route("/categorias/agregar", methods=["GET", "POST"])
@login_required
def agregar_categoria():
    if request.method == "POST":
        nombre = request.form["nombre"]
        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        flash("Categoría agregada correctamente.")
        return redirect(url_for("categorias.lista_categoria"))
    return render_template("categorias/agregar_categoria.html")


@categoria_blueprint.route("/categorias")
@login_required
def lista_categoria():
    categorias = Categoria.query.all()
    return render_template("categorias/lista_categoria.html", categorias=categorias)


@categoria_blueprint.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        categoria.nombre = request.form["nombre"]
        db.session.commit()
        flash("Categoría actualizada correctamente.")
        return redirect(url_for("categorias.lista_categoria"))
    return render_template("categorias/editar_categoria.html", categoria=categoria)


@categoria_blueprint.route("/categorias/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoría eliminada correctamente.")
    return redirect(url_for("categorias.lista_categoria"))
