from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        
        if not email or not password:
            flash('Please provide both email and password.', 'warning')
            return render_template('auth/login.html')
            
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            if user.preferred_language:
                session['locale'] = user.preferred_language
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
            
        flash('Invalid email or password. Please try again.', 'danger')
        
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        state = request.form.get('state', '').strip() or 'Telangana'
        district = request.form.get('district', '').strip() or 'Warangal'
        language = request.form.get('language', 'en')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', password)
        
        if not name or not email or not password:
            flash('Name, email, and password are required fields.', 'warning')
            return render_template('auth/register.html')
            
        if len(password) < 6:
            flash('Password should be at least 6 characters long.', 'warning')
            return render_template('auth/register.html')
            
        if confirm_password and password != confirm_password:
            flash('Passwords do not match. Please re-enter.', 'warning')
            return render_template('auth/register.html')
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address is already registered. Please log in.', 'info')
            return redirect(url_for('auth.login'))
            
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            state=state,
            district=district,
            preferred_language=language,
            is_admin=False
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        session['locale'] = language
        flash('Account registered successfully! Welcome to Smart Farmer AI.', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name).strip()
        current_user.phone = request.form.get('phone', current_user.phone).strip()
        current_user.state = request.form.get('state', current_user.state).strip()
        current_user.district = request.form.get('district', current_user.district).strip()
        lang = request.form.get('preferred_language', current_user.preferred_language)
        current_user.preferred_language = lang
        session['locale'] = lang
        
        new_pass = request.form.get('new_password', '').strip()
        if new_pass:
            if len(new_pass) >= 6:
                current_user.set_password(new_pass)
                flash('Password updated successfully.', 'success')
            else:
                flash('Password must be at least 6 characters.', 'warning')
                
        db.session.commit()
        flash('Profile details updated successfully.', 'success')
        return redirect(url_for('auth.profile'))
        
    return render_template('auth/profile.html')
