from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.usuario_model import Usuario
from database import db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        #rol = request.form['rol']
        if Usuario.query.filter_by(username=username).first():
            flash('Nombre de usuario ya existe.')
            return redirect(url_for('auth.registro'))

        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Ahora inicia sesión.')
        return redirect(url_for('auth.login'))

    return render_template('/registros/registro.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            return redirect(url_for('productos.lista_productos'))
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('auth.login'))

    return render_template('/registros/login.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('auth.login'))
