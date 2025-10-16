from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import json
import secrets
from datetime import datetime
import shutil

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

CONFIG_FILE = 'config.json'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_config():
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            'users': {
                'UPDATE_ADMIN_NAME': {
                    'password': generate_password_hash('UPDATE_ADMIN_PASSWORD'),
                    'role': 'admin',
                    'created_at': datetime.now().isoformat(),
                    'storage_used': 0
                }
            },
            'pending_requests': []
        }
        save_config(default_config)
        return default_config
    return load_config()

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        config = load_config()
        if config['users'][session['username']]['role'] != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_folder(username):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def calculate_folder_size(folder):
    total = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total

def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        config = load_config()
        
        if username in config['users'] and check_password_hash(config['users'][username]['password'], password):
            session['username'] = username
            session['role'] = config['users'][username]['role']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        config = load_config()
        
        if username in config['users']:
            flash('Username already exists.', 'danger')
        elif any(req['username'] == username for req in config['pending_requests']):
            flash('Registration request already pending.', 'warning')
        else:
            config['pending_requests'].append({
                'username': username,
                'password': generate_password_hash(password),
                'email': email,
                'requested_at': datetime.now().isoformat()
            })
            save_config(config)
            flash('Registration request submitted! Waiting for admin approval.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    config = load_config()
    is_admin = config['users'][username]['role'] == 'admin'
    
    if is_admin:
        # Admin sees all files from all users
        all_files = []
        total_storage = 0
        
        for user in config['users'].keys():
            user_folder = get_user_folder(user)
            if os.path.exists(user_folder):
                for filename in os.listdir(user_folder):
                    filepath = os.path.join(user_folder, filename)
                    if os.path.isfile(filepath):
                        file_size = os.path.getsize(filepath)
                        total_storage += file_size
                        all_files.append({
                            'name': filename,
                            'owner': user,
                            'size': format_size(file_size),
                            'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M'),
                            'is_own': user == username
                        })
        
        # Sort by modified date (newest first)
        all_files.sort(key=lambda x: x['modified'], reverse=True)
        
        return render_template('dashboard.html', 
                             username=username, 
                             files=all_files,
                             storage_used=format_size(total_storage),
                             role=session.get('role'),
                             is_admin=is_admin,
                             total_files=len(all_files))
    else:
        # Regular user sees only their files
        user_folder = get_user_folder(username)
        files = []
        
        for filename in os.listdir(user_folder):
            filepath = os.path.join(user_folder, filename)
            if os.path.isfile(filepath):
                files.append({
                    'name': filename,
                    'owner': username,
                    'size': format_size(os.path.getsize(filepath)),
                    'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M'),
                    'is_own': True
                })
        
        storage_used = calculate_folder_size(user_folder)
        config['users'][username]['storage_used'] = storage_used
        save_config(config)
        
        return render_template('dashboard.html', 
                             username=username, 
                             files=files,
                             storage_used=format_size(storage_used),
                             role=session.get('role'),
                             is_admin=is_admin,
                             total_files=len(files))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file selected'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file:
            filename = secure_filename(file.filename)
            
            # If secure_filename removes all characters, use a default name
            if not filename:
                filename = 'unnamed_file'
            
            user_folder = get_user_folder(session['username'])
            filepath = os.path.join(user_folder, filename)
            
            # Handle duplicate filenames
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filename = f"{base}_{counter}{ext}"
                filepath = os.path.join(user_folder, filename)
                counter += 1
            
            file.save(filepath)
            return jsonify({'success': True, 'message': f'File {filename} uploaded successfully'})
        
        return jsonify({'success': False, 'message': 'Upload failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Upload error: {str(e)}'})

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    user_folder = get_user_folder(session['username'])
    filepath = os.path.join(user_folder, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found.', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    user_folder = get_user_folder(session['username'])
    filepath = os.path.join(user_folder, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'success': True, 'message': 'File deleted successfully'})
    
    return jsonify({'success': False, 'message': 'File not found'})

@app.route('/admin')
@admin_required
def admin_panel():
    config = load_config()
    users_data = []
    all_files = []
    
    for username, data in config['users'].items():
        user_folder = get_user_folder(username)
        storage = calculate_folder_size(user_folder)
        file_count = len([f for f in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, f))])
        
        users_data.append({
            'username': username,
            'role': data['role'],
            'created_at': data.get('created_at', 'N/A'),
            'storage_used': format_size(storage),
            'file_count': file_count
        })
        
        # Collect all files from this user
        for filename in os.listdir(user_folder):
            filepath = os.path.join(user_folder, filename)
            if os.path.isfile(filepath):
                all_files.append({
                    'name': filename,
                    'owner': username,
                    'size': format_size(os.path.getsize(filepath)),
                    'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
                })
    
    # Sort files by modified date (newest first)
    all_files.sort(key=lambda x: x['modified'], reverse=True)
    
    return render_template('admin.html', 
                         users=users_data,
                         pending_requests=config['pending_requests'],
                         all_files=all_files)

@app.route('/admin/approve/<username>', methods=['POST'])
@admin_required
def approve_user(username):
    config = load_config()
    
    for req in config['pending_requests']:
        if req['username'] == username:
            config['users'][username] = {
                'password': req['password'],
                'role': 'user',
                'email': req['email'],
                'created_at': datetime.now().isoformat(),
                'storage_used': 0
            }
            config['pending_requests'].remove(req)
            save_config(config)
            return jsonify({'success': True, 'message': f'User {username} approved'})
    
    return jsonify({'success': False, 'message': 'Request not found'})

@app.route('/admin/deny/<username>', methods=['POST'])
@admin_required
def deny_user(username):
    config = load_config()
    
    for req in config['pending_requests']:
        if req['username'] == username:
            config['pending_requests'].remove(req)
            save_config(config)
            return jsonify({'success': True, 'message': f'User {username} denied'})
    
    return jsonify({'success': False, 'message': 'Request not found'})

@app.route('/admin/delete/<username>', methods=['POST'])
@admin_required
def delete_user(username):
    if username == 'admin':
        return jsonify({'success': False, 'message': 'Cannot delete admin account'})
    
    config = load_config()
    
    if username in config['users']:
        del config['users'][username]
        save_config(config)
        
        # Delete user folder
        user_folder = get_user_folder(username)
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
        
        return jsonify({'success': True, 'message': f'User {username} deleted'})
    
    return jsonify({'success': False, 'message': 'User not found'})

@app.route('/admin/download-file/<username>/<filename>')
@admin_required
def admin_download_file(username, filename):
    user_folder = get_user_folder(username)
    filepath = os.path.join(user_folder, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found.', 'danger')
        return redirect(url_for('admin_panel'))

@app.route('/admin/delete-file/<username>/<filename>', methods=['POST'])
@admin_required
def admin_delete_file(username, filename):
    user_folder = get_user_folder(username)
    filepath = os.path.join(user_folder, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'success': True, 'message': f'File deleted successfully from {username}\'s storage'})
    
    return jsonify({'success': False, 'message': 'File not found'})

@app.route('/admin/toggle-role/<username>', methods=['POST'])
@admin_required
def toggle_role(username):
    if username == 'admin':
        return jsonify({'success': False, 'message': 'Cannot modify admin role'})
    
    config = load_config()
    
    if username in config['users']:
        current_role = config['users'][username]['role']
        config['users'][username]['role'] = 'admin' if current_role == 'user' else 'user'
        save_config(config)
        return jsonify({'success': True, 'message': f'Role updated to {config["users"][username]["role"]}'})
    
    return jsonify({'success': False, 'message': 'User not found'})

if __name__ == '__main__':
    init_config()
    app.run(debug=True, host='0.0.0.0', port=5000)