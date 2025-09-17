from flask import Blueprint, jsonify, request
from app.controllers import paciente_controller

bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")

@bp.route("/", methods=["GET"])
def get_pacientes():
    """
    Função usada para criar uma rota do tipo GET para listar os pacientes do sistema
    :return: retorna os pacientes do banco de dados
    """
    try:
        pacientes = paciente_controller.listar_pacientes()
        return jsonify({
            "success": True,
            "data": [p.to_dict() for p in pacientes],
            "count": len(pacientes)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@bp.route("/<int:id>", methods=["GET"])
def get_paciente(id):
    """
    Função usada para criar uma rota do tipo GET para detalhar um paciente do sistema
    :param id: idetificador do paciente
    :return: retorna o paciente do banco de dados
    """
    try:
        paciente = paciente_controller.paciente_id(id)
        return jsonify({
            "success": True,
            "data": paciente.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404

@bp.route("/", methods=["POST"])
def post_paciente():
    """
    Função usada para criar uma rota do tipo PUT para atualizar os pacientes do sistema
    :return: faz a atualizacao do paciente no banco de dados
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400

        paciente = paciente_controller.criar_paciente(data)
        return jsonify({
            "success": True,
            "message": "Paciente criado com sucesso",
            "data": paciente.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@bp.route("/<int:id>", methods=["PUT"])
def put_paciente(id):
    """
    Função usada para criar uma rota do tipo PUT para atualizar os pacientes do sistema
    :param id: idetificador do paciente
    :return: faz a atualizacao do paciente no banco de dados
    """
    try:
        data = request.get_json()

        if not data:
            return  jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400

        paciente = paciente_controller.atualizar_paciente(id, data)
        return jsonify({
            "success": True,
            "message": "Paciente atualizado com sucesso",
            "data": paciente.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@bp.route("/<int:id>", methods=["DELETE"])
def delete_paciente(id):
    """
    Função usada para criar uma rota do tipo DELETE para remover os pacientes do sistema
    :param id: idetificador do paciente
    :return: faz a remocao do paciente no banco de dados
    """
    try:
        paciente_controller.deletar_paciente(id)
        return jsonify({
            "success": True,
            "message": "Paciente deletado com sucesso"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@bp.route("/buscar", methods=["GET"])
def search_paciente():
    """
    Função usada para criar uma rota do tipo GET para buscar pacientes pelo nome
    :return: retorna os pacientes do banco de dados que correspondem ao nome fornecido
    """
    try:
        nome = request.args.get("nome", "")
        if not nome:
            return jsonify({
                "success": False,
                "message": "Parâmetro 'nome' é obrigatório"
            }), 400

        pacientes = paciente_controller.paciente_nome(nome)
        return jsonify({
            "success": True,
            "data": [p.to_dict() for p in pacientes],
            "count": len(pacientes)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


@bp.route("/buscar/cpf", methods=["GET"])
def search_paciente_cpf():
    """
    Função usada para criar uma rota do tipo GET para buscar pacientes pelo CPF
    :return: retorna o paciente do banco de dados que corresponde ao CPF fornecido
    """
    try:
        cpf = request.args.get('cpf', '')
        if not cpf:
            return jsonify({
                "success": False,
                "message": "Parâmetro 'cpf' é obrigatório"
            }), 400

        paciente = paciente_controller.paciente_cpf(cpf)
        return jsonify({
            "success": True,
            "data": paciente.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404