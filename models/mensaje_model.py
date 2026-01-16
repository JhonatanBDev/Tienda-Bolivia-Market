# models/mensaje_model.py
from database import db
from datetime import datetime

class Mensaje(db.Model):
    __tablename__ = 'mensaje'

    id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)

    emisor = db.relationship("Usuario", foreign_keys=[emisor_id], back_populates="mensajes_enviados")
    receptor = db.relationship("Usuario", foreign_keys=[receptor_id], back_populates="mensajes_recibidos")
    