from app.extensions import db
class Medico(db.Model):
    __tablename__ = 'medicos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.Text, nullable=False)
    crm = db.Column(db.Text, nullable=False, unique=True)
    especialidade = db.Column(db.Text, nullable=False)
    telefone = db.Column(db.Text)
    email = db.Column(db.Text)
    criado_em = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    consultas = db.relationship("Consulta", back_populates="medico")

    def to_dict(self):
        """
        Convert Medico object to dictionary.
        :return: Dictionary representation of the Medico object.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "crm": self.crm,
            "especialidade": self.especialidade,
            "telefone": self.telefone,
            "email": self.email,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }