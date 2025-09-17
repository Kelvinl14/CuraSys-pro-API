from flask import Blueprint, jsonify, request
from app.controllers import exame_controller

bp = Blueprint("exames", __name__, url_prefix="/exames")

@bp.route("/", methods=["GET"])
def get_exames():
    """
    Retrieve all exams from the database.

    Returns:
        JSON response containing:
        - sucesso (bool): Indicates if the operation was successful.
        - exames (list): List of exams as dictionaries.
        - count (int): Total number of exams.
        - error (str): Error message if an exception occurs.
    """
    try:
        exames = exame_controller.listar_exames()
        return jsonify({
            "sucesso": True,
            "exames": [exame.as_dict() for exame in exames],
            "count": len(exames)
        }), 200
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 500

@bp.route("/<int:id>", methods=["GET"])
def get_exame(id):
    """
    Retrieve a specific exam by its ID.

    Args:
        id (int): Identifier of the exam.

    Returns:
        JSON response containing:
        - Exam data as a dictionary if found.
        - Error message if the exam is not found or an exception occurs.
    """
    try:
        exame = exame_controller.exame_id(id)
        if exame:
            return jsonify(exame.as_dict()), 200
        else:
            return jsonify({
                "sucesso": False,
                "error": "Exame não encontrado"}), 404
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 500

@bp.route("/", methods=["POST"])
def post_exame():
    """
    Create a new exam in the database.

    Request Body:
        JSON object containing exam data.

    Returns:
        JSON response containing:
        - Created exam data as a dictionary.
        - Error message if an exception occurs.
    """
    try:
        data = request.json
        exame = exame_controller.criar_exame(data)
        return jsonify({
            "sucesso": True,
            "exame": exame.as_dict()
        }), 201
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 500

@bp.route("/<int:id>", methods=["PUT"])
def put_exame(id):
    """
    Update an existing exam in the database.

    Args:
        id (int): Identifier of the exam to update.

    Request Body:
        JSON object containing updated exam data.

    Returns:
        JSON response containing:
        - Updated exam data as a dictionary.
        - Error message if an exception occurs.
    """
    try:
        data = request.json
        exame = exame_controller.atualizar_exame(id, data)
        return jsonify({
            "sucesso": True,
            "exame": exame.as_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 500

@bp.route("/<int:id>", methods=["DELETE"])
def delete_exame(id):
    """
    Delete an exam from the database.

    Args:
        id (int): Identifier of the exam to delete.

    Returns:
        JSON response containing:
        - Success message if the exam is deleted.
        - Error message if an exception occurs.
    """
    try:
        exame_controller.deletar_exame(id)
        return jsonify({
            "sucesso": True,
            "message": "Exame deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 500


@bp.route("/paciente/<int:id_paciente>", methods=["GET"])
def listar_exames_paciente(id_paciente):
    """
    Retrieve all exams for a specific patient.

    Args:
        id_paciente (int): Identifier of the patient.

    Returns:
        JSON response containing:
        - List of exams for the patient as dictionaries.
        - Error message if an exception occurs.
    """
    try:
        exames = exame_controller.listar_exames_paciente(id_paciente)
        return jsonify([exame.as_dict() for exame in exames]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/<int:id>/upload", methods=["POST"])
def upload_arquivo_exame(id):
    """
    Upload a file for a specific exam.

    Args:
        id (int): Identifier of the exam.

    Request Files:
        arquivo: The file to upload.

    Returns:
        JSON response containing:
        - Updated exam data as a dictionary.
        - Error message if an exception occurs or the file is invalid.
    """
    try:
        if 'arquivo' not in request.files:
            return jsonify({"error": "Nenhum arquivo fornecido"}), 400

        arquivo = request.files['arquivo']
        if arquivo.filename == '':
            return jsonify({"error": "Nome do arquivo vazio"}), 400

        # Salvar o arquivo em um diretório específico
        caminho_arquivo = f"uploads/{arquivo.filename}"
        arquivo.save(caminho_arquivo)

        exame = exame_controller.upload_arquivo_exame(id, caminho_arquivo)
        return jsonify(exame.as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500