from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.user import UserCreateSchema, UserLoginSchema
from app.services.auth_service import AuthService
from app.middleware.auth_middleware import jwt_required as require_auth

bp = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

@bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    try:
        data = request.get_json()
        schema = UserCreateSchema(**data)
        result, status_code = AuthService.register(schema.dict())
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422

@bp.route('/login', methods=['POST'])
@limiter.limit("10 per 15 minutes")
def login():
    try:
        data = request.get_json()
        schema = UserLoginSchema(**data)
        result, status_code = AuthService.login(schema.dict())
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422

@bp.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 400
    
    result, status_code = AuthService.refresh_token(refresh_token)
    return jsonify(result), status_code

@bp.route('/logout', methods=['POST'])
def logout():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 400
    
    result, status_code = AuthService.logout(refresh_token)
    return jsonify(result), status_code

@bp.route('/me', methods=['GET'])
@require_auth
def get_profile():
    from flask import g
    return jsonify(g.current_user.to_dict()), 200