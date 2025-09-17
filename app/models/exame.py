from app.extensions import db

class Exame(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    tipo = db.Column(db.Text, nullable=False)
    resultado = db.Column(db.Text)
    arquivo_exame = db.Column(db.Text)
    criado_em = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    paciente = db.relationship("Paciente", back_populates="exames")

    def to_dict(self):
        """
        Convert Exame object to dictionary.
        :return: Dictionary representation of the Exame object.
        """
        return {
            "id": self.id,
            "id_paciente": self.id_paciente,
            "tipo": self.tipo,
            "resultado": self.resultado,
            "arquivo_exame": self.arquivo_exame,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }