from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from passlib.hash import bcrypt
from datetime import timedelta
import uuid

from app.models.user import User
from app.models.token import RefreshToken
from app.models.category import Category
from app.database import db

class AuthService:
    
    @staticmethod
    def register(user_data):
        # Check if user exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            return {'error': 'Email already registered'}, 409
        
        # Hash password
        hashed_password = bcrypt.hash(user_data['password'])
        
        # Create user
        user = User(
            id=str(uuid.uuid4()),
            name=user_data['name'],
            email=user_data['email'],
            password=hashed_password
        )
        
        db.session.add(user)
        db.session.flush()
        
        # Create default categories for new user
        default_categories = [
            Category(id=str(uuid.uuid4()), name='Work', color='#FF6B6B', user_id=user.id, is_default=True),
            Category(id=str(uuid.uuid4()), name='Personal', color='#4ECDC4', user_id=user.id, is_default=True),
            Category(id=str(uuid.uuid4()), name='Shopping', color='#45B7D1', user_id=user.id, is_default=True)
        ]
        
        for category in default_categories:
            db.session.add(category)
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=7)
        )
        
        # Store refresh token
        refresh_token_obj = RefreshToken(
            id=str(uuid.uuid4()),
            token=refresh_token,
            user_id=user.id,
            expires_at=timedelta(days=7)
        )
        db.session.add(refresh_token_obj)
        db.session.commit()
        
        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201
    
    @staticmethod
    def login(credentials):
        user = User.query.filter_by(email=credentials['email']).first()
        
        if not user or not bcrypt.verify(credentials['password'], user.password):
            return {'error': 'Invalid credentials'}, 401
        
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=7)
        )
        
        # Store refresh token
        refresh_token_obj = RefreshToken(
            id=str(uuid.uuid4()),
            token=refresh_token,
            user_id=user.id,
            expires_at=timedelta(days=7)
        )
        db.session.add(refresh_token_obj)
        db.session.commit()
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'
        }, 200
    
    @staticmethod
    def refresh_token(refresh_token):
        token = RefreshToken.query.filter_by(
            token=refresh_token,
            revoked=False
        ).first()
        
        if not token:
            return {'error': 'Invalid refresh token'}, 401
        
        new_access_token = create_access_token(
            identity=token.user_id,
            expires_delta=timedelta(minutes=15)
        )
        
        return {'access_token': new_access_token}, 200
    
    @staticmethod
    def logout(refresh_token):
        token = RefreshToken.query.filter_by(token=refresh_token).first()
        if token:
            token.revoked = True
            db.session.commit()
        
        return {'message': 'Logged out successfully'}, 200