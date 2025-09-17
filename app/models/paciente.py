from app.extensions import db

class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    consultas = db.relationship("Consulta", back_populates="paciente", lazy=True)
    exames = db.relationship("Exame", back_populates="paciente", lazy=True)

    def to_dict(self):
        """
        Convert Paciente object to dictionary.
        :return: Dictionary representation of the Paciente object.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "email": self.email,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }