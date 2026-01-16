# models/compra_model.py
from database import db
from datetime import datetime

class Compra(db.Model):
    __tablename__ = 'compra'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    pagado = db.Column(db.Boolean, default=False)

    # Relaciones (opcional para consultas más fáciles)
    usuario = db.relationship('Usuario', back_populates='compras')
    producto = db.relationship('Producto')
    detalles = db.relationship("DetalleCompra", back_populates="compra", cascade="all, delete-orphan")
