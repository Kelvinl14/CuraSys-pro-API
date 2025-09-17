from flask import Blueprint, jsonify, request
from app.controllers import medico_controller

bp = Blueprint("medicos", __name__, url_prefix="/medicos")

@bp.route("/", methods=["GET"])
def get_medicos():
    """
    Função usada para criar uma rota do tipo GET para listar os medicos do sistema
    :return: retorna os medicos do banco de dados
    """
    try:
        pacientes = medico_controller.listar_medicos()
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
def get_medico(id):
    """
    Função usada para criar uma rota do tipo GET para detalhar um medico do sistema
    :param id: idetificador do medico
    :return: retorna o medico do banco de dados
    """
    try:
        medico = medico_controller.medico_id(id)
        return jsonify({
            "success": True,
            "data": medico.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404

@bp.route("/", methods=["POST"])
def post_medico():
    """
    Função usada para criar uma rota do tipo PUT para atualizar os medicos do sistema
    :return: faz a atualizacao do medico no banco de dados
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400

        paciente = medico_controller.criar_medico(data)
        return jsonify({
            "success": True,
            "message": "Medico criado com sucesso",
            "data": paciente.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@bp.route("/<int:id>", methods=["PUT"])
def put_medico(id):
    """
    Função usada para criar uma rota do tipo PUT para atualizar os medicos do sistema
    :param id: idetificador do medico
    :return: faz a atualizacao do medico no banco de dados
    """
    try:
        data = request.get_json()

        if not data:
            return  jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400

        paciente = medico_controller.atualizar_medico(id, data)
        return jsonify({
            "success": True,
            "message": "Medico atualizado com sucesso",
            "data": paciente.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@bp.route("/<int:id>", methods=["DELETE"])
def delete_medico(id):
    """
    Função usada para criar uma rota do tipo DELETE para remover os medicos do sistema
    :param id: idetificador do medico
    :return: faz a remocao do medico no banco de dados
    """
    try:
        medico_controller.deletar_medico(id)
        return jsonify({
            "success": True,
            "message": "Medico deletado com sucesso"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@bp.route("/buscar", methods=["GET"])
def search_medico():
    """
    Função usada para criar uma rota do tipo GET para buscar medicos pelo nome
    :return: retorna os medicos do banco de dados que correspondem ao nome fornecido
    """
    try:
        nome = request.args.get("nome", "")
        if not nome:
            return jsonify({
                "success": False,
                "message": "Parâmetro 'nome' é obrigatório"
            }), 400

        medicos = medico_controller.medico_nome(nome)
        return jsonify({
            "success": True,
            "data": [m.to_dict() for m in medicos],
            "count": len(medicos)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


@bp.route("/buscar/cpf", methods=["GET"])
def search_medico_cpf():
    """
    Função usada para criar uma rota do tipo GET para buscar medicos pelo CPF
    :return: retorna o medico do banco de dados que corresponde ao CPF fornecido
    """
    try:
        cpf = request.args.get('cpf', '')
        if not cpf:
            return jsonify({
                "success": False,
                "message": "Parâmetro 'cpf' é obrigatório"
            }), 400

        medico = medico_controller.medico_cpf(cpf)
        return jsonify({
            "success": True,
            "data": medico.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404

@bp.route("/buscar/crm", methods=["GET"])
def search_medico_crm():
    """
    Função usada para criar uma rota do tipo GET para buscar medicos pelo CRM
    :return: retorna o medico do banco de dados que corresponde ao CRM fornecido
    """
    try:
        crm = request.args.get('crm', '')
        if not crm:
            return jsonify({
                "success": False,
                "message": "Parâmetro 'crm' é obrigatório"
            }), 400

        medico = medico_controller.medico_crm(crm)
        return jsonify({
            "success": True,
            "data": medico.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404

@bp.route("/filtrar", methods=["GET"])
def filter_medicos():
    """
    Função usada para criar uma rota do tipo GET para filtrar medicos por especialidade
    :return: retorna os medicos do banco de dados que correspondem a especialidade fornecida
    """
    try:
        especialidade = request.args.get("especialidade", "")
        if not especialidade:
            return jsonify({
                "success": False,
                "message": "Parâmetro 'especialidade' é obrigatório"
            }), 400

        medicos = medico_controller.medico_especialidade(especialidade)
        return jsonify({
            "success": True,
            "data": [m.to_dict() for m in medicos],
            "count": len(medicos)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400