from app.extensions import db
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Text, nullable=False, server_default='admin')
    criado_em = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.set_password(password)

    def set_password(self, password):
        self.senha_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.senha_hash.encode('utf-8'))

    def to_dict(self):
        """
        Convert User object to dictionary.
        :return: Dictionary representation of the User object.
        """
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "role": self.role,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }