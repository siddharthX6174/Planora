from flask import Blueprint, request, jsonify, g
from app.middleware.auth_middleware import jwt_required
from app.services.task_service import TaskService
from app.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskStatusUpdateSchema

bp = Blueprint('tasks', __name__)

@bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    # Get filters from query params
    filters = {
        'status': request.args.get('status'),
        'priority': request.args.get('priority'),
        'category_id': request.args.get('category_id')
    }
    
    # Pagination
    pagination = {
        'page': int(request.args.get('page', 1)),
        'limit': int(request.args.get('limit', 10))
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    result, status_code = TaskService.get_tasks(filters, pagination)
    return jsonify(result), status_code

@bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = request.get_json()
        schema = TaskCreateSchema(**data)
        result, status_code = TaskService.create_task(schema.dict(exclude_none=True))
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422

@bp.route('/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    result, status_code = TaskService.get_task(task_id)
    return jsonify(result), status_code

@bp.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        data = request.get_json()
        schema = TaskUpdateSchema(**data)
        result, status_code = TaskService.update_task(task_id, schema.dict(exclude_none=True))
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422

@bp.route('/<task_id>/status', methods=['PATCH'])
@jwt_required()
def update_task_status(task_id):
    try:
        data = request.get_json()
        schema = TaskStatusUpdateSchema(**data)
        result, status_code = TaskService.update_status(task_id, schema.dict())
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 422

@bp.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    result, status_code = TaskService.delete_task(task_id)
    if status_code == 204:
        return '', 204
    return jsonify(result), status_code

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_tasks():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    result, status_code = TaskService.search_tasks(query)
    return jsonify(result), status_code

@bp.route('/<task_id>/assign', methods=['POST'])
@jwt_required()
def assign_task(task_id):
    assignee_id = request.json.get('user_id')
    if not assignee_id:
        return jsonify({'error': 'User ID required'}), 400
    
    result, status_code = TaskService.assign_task(task_id, assignee_id)
    return jsonify(result), status_code