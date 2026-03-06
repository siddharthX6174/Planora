from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.models.user import User
from passlib.hash import pbkdf2_sha256 as pwd_context
from app.services.auth_service import AuthService

# Create blueprint for frontend routes
frontend_bp = Blueprint('frontend', __name__)

# Login required decorator for frontend routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('frontend.login'))
        return f(*args, **kwargs)
    return decorated_function

# Index/Home page
@frontend_bp.route('/')
def index():
    return render_template('index.html')

# Login page
@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Authenticate user against the database
        user = User.query.filter_by(email=email).first()
        if not user or not pwd_context.verify(password, user.password):
            flash('Invalid credentials', 'danger')
            return render_template('login.html')

        # Store minimal user info in session
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.name

        # Generate JWT access + refresh tokens for SPA API calls
        auth_result, auth_status = AuthService.login({'email': email, 'password': password})
        if auth_status == 200:
            session['access_token'] = auth_result.get('access_token')
            session['refresh_token'] = auth_result.get('refresh_token')

        flash('Login successful!', 'success')
        return redirect(url_for('frontend.dashboard'))
    
    return render_template('login.html')

# Register page
@frontend_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        # Register user using AuthService
        try:
            payload = {'name': name, 'email': email, 'password': password}
            result, status = AuthService.register(payload)
            if status == 201:
                # auto-login the new user in session
                user = result.get('user')
                session['user_id'] = user.get('id')
                session['user_email'] = user.get('email')
                session['user_name'] = user.get('name')

                # Save access/refresh tokens so frontend JS can call protected APIs
                session['access_token'] = result.get('access_token')
                session['refresh_token'] = result.get('refresh_token')

                flash('Registration successful! You are now logged in.', 'success')
                return redirect(url_for('frontend.dashboard'))
            else:
                flash(result.get('error', 'Registration failed'), 'danger')
                return render_template('register.html')
        except Exception as e:
            flash('Registration failed: ' + str(e), 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

# Dashboard page
@frontend_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Tasks page
@frontend_bp.route('/tasks')
@login_required
def tasks():
    return render_template('tasks.html')

# Categories page
@frontend_bp.route('/categories')
@login_required
def categories():
    return render_template('categories.html')

# User profile page
@frontend_bp.route('/profile')
@login_required
def profile():
    user = None
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)

    return render_template('profile.html', user=user)

# Logout
@frontend_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('frontend.index'))
