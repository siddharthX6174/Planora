from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

from app.config import Config
from app.database import db, init_db

# Import routes
from app.routes import auth_routes, task_routes, user_routes, category_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    init_db(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Register blueprints
    app.register_blueprint(auth_routes.bp, url_prefix='/api/v1/auth')
    app.register_blueprint(task_routes.bp, url_prefix='/api/v1/tasks')
    app.register_blueprint(user_routes.bp, url_prefix='/api/v1/users')
    app.register_blueprint(category_routes.bp, url_prefix='/api/v1/categories')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)