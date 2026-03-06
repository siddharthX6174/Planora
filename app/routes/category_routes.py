from flask import Blueprint, request, jsonify, g
from app.middleware.auth_middleware import jwt_required
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreateSchema

bp = Blueprint('categories', __name__)

@bp.route('', methods=['GET'])
@jwt_required
def get_categories():
    result, status_code = CategoryService.get_categories(g.current_user.id)
    return jsonify(result), status_code

@bp.route('', methods=['POST'])
@jwt_required
def create_category():
    try:
        data = request.get_json()
        schema = CategoryCreateSchema(**data)
        result, status_code = CategoryService.create_category(
            g.current_user.id,
            schema.dict()
        )
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422

@bp.route('/<category_id>', methods=['DELETE'])
@jwt_required
def delete_category(category_id):
    result, status_code = CategoryService.delete_category(
        g.current_user.id,
        category_id
    )
    if status_code == 204:
        return '', 204
    return jsonify(result), status_code
@bp.route('/<category_id>', methods=['PUT'])
@jwt_required
def update_category(category_id):
    try:
        data = request.get_json()
        result, status_code = CategoryService.update_category(
            g.current_user.id,
            category_id,
            data
        )
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422
