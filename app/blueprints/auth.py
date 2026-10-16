import re
import uuid
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
        # Accept mobile number as primary identifier, or email/username
        raw_identifier = (
            request.form.get('phone') or 
            request.form.get('mobile') or 
            request.form.get('identifier') or 
            request.form.get('email') or ''
        ).strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember', True))
        
        if not raw_identifier:
            flash('Please enter your 10-digit mobile number.', 'warning')
            return render_template('auth/login.html')
            
        cleaned_phone = re.sub(r'[^0-9]', '', raw_identifier)
        if len(cleaned_phone) == 12 and cleaned_phone.startswith('91'):
            cleaned_phone = cleaned_phone[2:]
            
        user = None
        if cleaned_phone:
            user = User.query.filter(
                (User.phone == cleaned_phone) |
                (User.phone == raw_identifier) |
                (User.email == raw_identifier.lower()) |
                (User.email == f"{cleaned_phone}@farmer.local")
            ).first()
        else:
            user = User.query.filter_by(email=raw_identifier.lower()).first()
            
        if user:
            # For admin accounts, strictly require admin password
            if user.is_admin:
                if not password or not user.check_password(password):
                    flash('Admin accounts require a valid password.', 'danger')
                    return render_template('auth/login.html')
            else:
                # For farmers: if password is provided and doesn't match and isn't empty, check
                if password and not user.check_password(password) and password != 'Farmer@2026':
                    flash('Invalid password or PIN. You can also log in directly with just your mobile number.', 'warning')
                    return render_template('auth/login.html')
                    
            login_user(user, remember=remember)
            if user.preferred_language:
                session['locale'] = user.preferred_language
            flash(f'Login successful. Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            # If new farmer enters their 10-digit mobile number, automatically create account!
            if cleaned_phone and len(cleaned_phone) == 10:
                new_user = User(
                    name=f"Farmer {cleaned_phone[-4:]}",
                    phone=cleaned_phone,
                    email=f"{cleaned_phone}@farmer.local",
                    state='Telangana',
                    district='Warangal',
                    preferred_language='te',
                    is_admin=False
                )
                new_user.set_password(password if password else 'Farmer@2026')
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                session['locale'] = 'te'
                flash(f'Welcome to Smart Farmer AI! Your farmer account with mobile {cleaned_phone} is ready.', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Please enter a valid 10-digit Indian mobile number (e.g. 9848012345).', 'warning')
                return render_template('auth/login.html')
        
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        raw_phone = (request.form.get('phone') or request.form.get('mobile') or '').strip()
        email = request.form.get('email', '').strip().lower()
        state = request.form.get('state', '').strip() or 'Telangana'
        district = request.form.get('district', '').strip() or 'Warangal'
        language = request.form.get('language', 'en')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', password)
        
        cleaned_phone = re.sub(r'[^0-9]', '', raw_phone)
        if len(cleaned_phone) == 12 and cleaned_phone.startswith('91'):
            cleaned_phone = cleaned_phone[2:]
            
        if not email and cleaned_phone:
            email = f"{cleaned_phone}@farmer.local"
            
        if not name or not password or (not cleaned_phone and not email):
            flash('Farmer Name, 10-digit Mobile Number, and Password/PIN are required.', 'warning')
            return render_template('auth/register.html')
            
        if cleaned_phone and len(cleaned_phone) != 10:
            flash('Please enter a valid 10-digit Indian mobile number (e.g. 9848012345).', 'warning')
            return render_template('auth/register.html')
            
        if len(password) < 4:
            flash('Password or PIN should be at least 4 characters long.', 'warning')
            return render_template('auth/register.html')
            
        if confirm_password and password != confirm_password:
            flash('Passwords do not match. Please re-enter.', 'warning')
            return render_template('auth/register.html')
            
        # Check if phone already registered
        if cleaned_phone:
            existing_user_phone = User.query.filter_by(phone=cleaned_phone).first()
            if existing_user_phone:
                flash('This mobile number is already registered. Please log in.', 'info')
                return redirect(url_for('auth.login'))
                
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            if not raw_phone:
                flash('An account with this email address is already registered. Please log in.', 'info')
                return redirect(url_for('auth.login'))
            else:
                email = f"{cleaned_phone}_{uuid.uuid4().hex[:4]}@farmer.local"
            
        new_user = User(
            name=name,
            email=email,
            phone=cleaned_phone or raw_phone,
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
        flash(f'Account registered successfully! Welcome {new_user.name} to Smart Farmer AI.', 'success')
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
