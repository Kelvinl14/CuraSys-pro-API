from app.extensions import db

class Consulta(db.Model):
    __tablename__ = "consultas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data_consulta = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('agendada', 'realizada', 'cancelada', name='status_consulta'), server_default='agendada')  # agendada, realizada, cancelada
    criado_em = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Relacionamentos
    paciente = db.relationship("Paciente", back_populates="consultas")
    medico = db.relationship("Medico", back_populates="consultas")

    def to_dict(self):
        """
        Convert Consulta object to dictionary.
        :return: Dictionary representation of the Consulta object.
        """
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id,
            "data_consulta": self.data_consulta.isoformat() if self.data_consulta else None,
            "status": self.status,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }