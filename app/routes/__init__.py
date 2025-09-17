from .user_routes import bp as user_bp
from .paciente_routes import bp as paciente_bp
from .medico_routes import bp as medico_bp
from .consulta_routes import bp as consulta_bp
from .exame_routes import bp as exame_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(medico_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(exame_bp)
