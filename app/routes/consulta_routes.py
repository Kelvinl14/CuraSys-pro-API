from flask import Blueprint, jsonify, request
from app.controllers import consulta_controller

bp = Blueprint("consultas", __name__, url_prefix="/consultas")

@bp.route("/", methods=["GET"])
def listar_consultas():
    """
    Retrieve a list of all consultations.

    This function interacts with the `consulta_controller` to fetch all consultations
    from the database. The consultations are then converted to dictionaries for JSON serialization.

    Returns:
        Response: A JSON response containing:
            - sucesso (bool): Indicates if the operation was successful.
            - consultas (list): A list of consultations as dictionaries.
            - count (int): The total number of consultations.
        HTTP Status Codes:
            - 200: If the consultations are successfully retrieved.
            - 500: If an exception occurs during the process.
    """
    try:
        consultas = consulta_controller.listar_consultas()
        consultas_data = [consulta.to_dict() for consulta in consultas]
        return jsonify({
            "sucesso": True,
            "consultas": consultas_data,
            "count": len(consultas_data)
        }), 200
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 500

@bp.route("/<int:id>", methods=["GET"])
def consulta_por_id(id):
    """
    Retrieve a specific consultation by its ID.

    Args:
        id (int): Identifier of the consultation.

    Returns:
        Response: A JSON response containing:
            - success (bool): Indicates if the operation was successful.
            - data (dict): The consultation data as a dictionary.
        HTTP Status Codes:
            - 200: If the consultation is successfully retrieved.
            - 404: If the consultation is not found or an exception occurs.
    """
    try:
        consulta = consulta_controller.consulta_id(id)
        return jsonify({
            "success": True,
            "data": consulta.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)}), 404

@bp.route("/", methods=["POST"])
def criar_consulta():
    """
    Create a new consultation.

    Request Body:
        JSON object containing the consultation data.

    Returns:
        Response: A JSON response containing:
            - success (bool): Indicates if the operation was successful.
            - data (dict): The created consultation data as a dictionary.
        HTTP Status Codes:
            - 201: If the consultation is successfully created.
            - 400: If an exception occurs during the process.
    """
    try:
        data = request.get_json()
        consulta = consulta_controller.criar_consulta(data)
        return jsonify({
            "success": True,
            "data": consulta.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)}), 400

@bp.route("/<int:id>", methods=["PUT"])
def atualizar_consulta(id):
    """
    Update an existing consultation.

    Args:
        id (int): Identifier of the consultation to update.

    Request Body:
        JSON object containing the updated consultation data.

    Returns:
        Response: A JSON response containing:
            - success (bool): Indicates if the operation was successful.
            - data (dict): The updated consultation data as a dictionary.
        HTTP Status Codes:
            - 200: If the consultation is successfully updated.
            - 400: If an exception occurs during the process.
    """
    try:
        data = request.get_json()
        consulta = consulta_controller.atualizar_consulta(id, data)
        return jsonify({
            "success": True,
            "data": consulta.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)}), 400

@bp.route("/<int:id>", methods=["DELETE"])
def deletar_consulta(id):
    """
    Delete a consultation.

    Args:
        id (int): Identifier of the consultation to delete.

    Returns:
        Response: A JSON response containing:
            - success (bool): Indicates if the operation was successful.
            - message (str): A success message if the consultation is deleted.
        HTTP Status Codes:
            - 200: If the consultation is successfully deleted.
            - 400: If an exception occurs during the process.
    """
    try:
        consulta_controller.deletar_consulta(id)
        return jsonify({
            "success": True,
            "message": "Consulta deletada com sucesso"}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)}), 400

@bp.route("/paciente/<int:paciente_id>", methods=["GET"])
def listar_consultas_por_paciente(paciente_id):
    """
    Retrieve all consultations for a specific patient.

    Args:
        paciente_id (int): Identifier of the patient.

    Returns:
        Response: A JSON response containing:
            - sucesso (bool): Indicates if the operation was successful.
            - consultas (list): A list of consultations for the patient as dictionaries.
            - count (int): The total number of consultations for the patient.
        HTTP Status Codes:
            - 200: If the consultations are successfully retrieved.
            - 400: If an exception occurs during the process.
    """
    try:
        consultas = consulta_controller.listar_consultas_por_paciente(paciente_id)
        consultas_data = [consulta.to_dict() for consulta in consultas]
        return jsonify({
            "sucesso": True,
            "consultas": consultas_data,
            "count": len(consultas_data)
        }), 200
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 400


@bp.route("/medico/<int:medico_id>", methods=["GET"])
def listar_consultas_por_medico(medico_id):
    """
    Retrieve all consultations for a specific doctor.

    Args:
        medico_id (int): Identifier of the doctor.

    Returns:
        Response: A JSON response containing:
            - sucesso (bool): Indicates if the operation was successful.
            - consultas (list): A list of consultations for the doctor as dictionaries.
            - count (int): The total number of consultations for the doctor.
        HTTP Status Codes:
            - 200: If the consultations are successfully retrieved.
            - 400: If an exception occurs during the process.
    """
    try:
        consultas = consulta_controller.listar_consultas_por_medico(medico_id)
        consultas_data = [consulta.to_dict() for consulta in consultas]
        return jsonify({
            "sucesso": True,
            "consultas": consultas_data,
            "count": len(consultas_data)
        }), 200
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": str(e)}), 400