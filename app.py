from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a strong random key in production

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User database (replace with real database in production)
users = {
    "M": {
        "pharmacy_code": "M1",
        "password": generate_password_hash("M"),
        "locked": False,
        "failed_attempts": 0,
        "lock_time": None
    }
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if account is locked first
        username = request.form.get('username') if request.form else request.get_json().get('username')
        user_data = users.get(username)
        
        if user_data and user_data['locked']:
            if user_data['lock_time'] and datetime.now() < user_data['lock_time']:
                message = "Account locked. Try again later."
                if request.headers.get('Content-Type') == 'application/json':
                    return jsonify({
                        'success': False,
                        'locked': True,
                        'message': message,
                        'lock_time': user_data['lock_time'].isoformat()
                    })
                flash(message, 'error')
                return render_template('auth/login.html')
            else:
                # Lock expired
                user_data['locked'] = False
                user_data['failed_attempts'] = 0
                user_data['lock_time'] = None

        # Process login attempt
        pharmacy_code = request.form.get('pharmacyCode') if request.form else request.get_json().get('pharmacyCode')
        password = request.form.get('password') if request.form else request.get_json().get('password')
        
        # Validate credentials
        if user_data and user_data['pharmacy_code'] == pharmacy_code:
            if check_password_hash(user_data['password'], password):
                login_user(User(username))
                if request.headers.get('Content-Type') == 'application/json':
                    return jsonify({'success': True, 'redirect': url_for('dashboard')})
                return redirect(url_for('dashboard'))
            else:
                # Failed attempt
                user_data['failed_attempts'] += 1
                
                if user_data['failed_attempts'] >= 3:
                    user_data['locked'] = True
                    user_data['lock_time'] = datetime.now() + timedelta(minutes=5)
                    message = "Too many failed attempts. Account locked for 5 minutes."
                else:
                    message = f"Invalid credentials. {3 - user_data['failed_attempts']} attempts remaining."
                
                if request.headers.get('Content-Type') == 'application/json':
                    return jsonify({
                        'success': False,
                        'locked': user_data['locked'],
                        'message': message,
                        'attempts_left': 3 - user_data['failed_attempts']
                    })
                flash(message, 'error')
        else:
            message = "Invalid pharmacy code or username"
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')

        return render_template('auth/login.html') if request.form else jsonify({'success': False, 'message': message})
    
    # GET request - show login page
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.id)

@app.route('/api/check_lock_status')
def check_lock_status():
    username = request.args.get('username')
    user_data = users.get(username, {})
    
    if user_data.get('locked') and user_data.get('lock_time'):
        remaining = (user_data['lock_time'] - datetime.now()).total_seconds()
        if remaining > 0:
            return jsonify({
                'locked': True,
                'remaining_time': remaining,
                'message': f"Account locked. {int(remaining//60)}m {int(remaining%60)}s remaining"
            })
        else:
            # Lock expired
            user_data['locked'] = False
            user_data['failed_attempts'] = 0
            user_data['lock_time'] = None
    
    return jsonify({'locked': False})

if __name__ == '__main__':
    app.run(debug=True)