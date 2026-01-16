from database import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # 👉 Agregado
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default='cliente', nullable=False)

    compras = db.relationship('Compra', back_populates='usuario', cascade="all, delete-orphan")
    comentarios = db.relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")
    productos = db.relationship("Producto", back_populates="usuario")
    favoritos = db.relationship("Favorito", back_populates="usuario", cascade="all, delete-orphan")
    mensajes_enviados = db.relationship("Mensaje", foreign_keys='Mensaje.emisor_id', back_populates="emisor", cascade="all, delete-orphan")
    mensajes_recibidos = db.relationship("Mensaje", foreign_keys='Mensaje.receptor_id', back_populates="receptor", cascade="all, delete-orphan")
   


