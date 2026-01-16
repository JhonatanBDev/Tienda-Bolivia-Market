# models/direccion_model.py
from database import db

class DireccionEnvio(db.Model):
    __tablename__ = 'direccion_envio'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(100))
    pais = db.Column(db.String(100), default="Bolivia")
    telefono = db.Column(db.String(20))

    usuario = db.relationship("Usuario", backref="direcciones_envio")
