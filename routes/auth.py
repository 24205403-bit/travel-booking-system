from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.find_by_email(email)
        if user and User.verify_password(user['password'], password):
            session['user_id'] = user['_id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user.get('role', 'user')
            flash(f"Welcome back, {user['name']}!", 'success')
            next_url = request.args.get('next')
            if user.get('role') == 'admin':
                return redirect(next_url or url_for('admin.dashboard'))
            return redirect(next_url or url_for('main.index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        role = request.form.get('role', 'user')  # Option to register as user or admin for testing

        if not name or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('auth/register.html')

        existing_user = User.find_by_email(email)
        if existing_user:
            flash('Email address already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        user = User.create(name, email, password, phone, role)
        session['user_id'] = user['_id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        flash('Account created successfully! Welcome to TravelExplorer.', 'success')

        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.index'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
