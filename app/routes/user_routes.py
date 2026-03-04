from flask import Blueprint, request, jsonify, g
from app.middleware.auth_middleware import jwt_required
from app.services.user_service import UserService
from app.schemas.user import UserUpdateSchema, PasswordChangeSchema

bp = Blueprint('users', __name__)

@bp.route('/me', methods=['GET'])
@jwt_required
def get_profile():
    return jsonify(g.current_user.to_dict()), 200

@bp.route('/me', methods=['PUT'])
@jwt_required
def update_profile():
    try:
        data = request.get_json()
        schema = UserUpdateSchema(**data)
        result, status_code = UserService.update_profile(g.current_user.id, schema.dict(exclude_none=True))
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422

@bp.route('/me/password', methods=['PUT'])
@jwt_required
def change_password():
    try:
        data = request.get_json()
        schema = PasswordChangeSchema(**data)
        result, status_code = UserService.change_password(
            g.current_user.id,
            schema.dict()
        )
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422