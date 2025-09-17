from flask import Blueprint, jsonify, request
from app.models.user import User
from app.controllers import user_controller

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def get_users():
    try:
        users = user_controller.listar_usuarios()
        return jsonify({
            "success": True,
            "data": [u.to_dict() for u in users],
            "count": len(users)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = user_controller.usuario_id(id)
        return jsonify({
            "success": True,
            "data": user.to_dict()
        }), 200
    except Exception as e:
        if "não encontrado" in str(e).lower() or "not found" in str(e).lower():
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
@bp.route("/", methods=["POST"])
def post_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400

        # Validação básica
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "success": False,
                    "error": f"Field '{field}' is required"
                }), 400

        user = user_controller.criar_usuario(data)
        return jsonify({
            "success": True,
            "data": user.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@bp.route("/<int:id>", methods=["PUT"])
def put_user(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"}), 400

        user = user_controller.atualizar_usuario(id, data)
        return jsonify({
            "success": True,
            "data": user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)}), 500

@bp.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user_controller.deletar_usuario(id)
        return jsonify({
            "success": True,
            "message": "User deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)}), 500
