from database import db

class Carrito(db.Model):
    __tablename__ = 'carrito'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    # Relaciones
    producto = db.relationship('Producto')
    usuario = db.relationship('Usuario')  # <- para acceder como item.usuario.username
