# models/favorito_model.py
from database import db
from flask_login import UserMixin

class Favorito(db.Model):
    __tablename__ = 'favorito'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)

    # Relaciones opcionales para facilitar consultas (no obligatorias)
    usuario = db.relationship("Usuario", back_populates="favoritos")
    producto = db.relationship("Producto", back_populates="favoritos")
    
