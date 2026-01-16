# models/detalle_compra_model.py
from database import db

class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compra'

    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    # Relaciones
    compra = db.relationship("Compra", back_populates="detalles")
    producto = db.relationship("Producto")
