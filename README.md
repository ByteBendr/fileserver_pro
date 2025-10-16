# 🚀 FileServer Pro

A professional, secure, and feature-rich file server application built with Flask. Features modern UI, role-based access control, admin oversight, and comprehensive file management capabilities.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

### 🔐 Security & Authentication
- **Secure Login System** - Password hashing with Werkzeug
- **Registration Approval Workflow** - Admins approve new users
- **Session Management** - Secure session handling
- **Role-Based Access Control** - Admin and user roles
- **File Isolation** - Each user has their own secure folder

### 📁 File Management
- **Drag & Drop Upload** - Modern file upload interface
- **Multiple File Upload** - Upload multiple files at once
- **All File Types Supported** - No restrictions on file types
- **File Download** - Easy file retrieval
- **File Deletion** - Remove unwanted files
- **Duplicate Handling** - Auto-rename duplicate files

### 👑 Admin Features
- **User Management** - Create, delete, and modify users
- **Registration Approval** - Review and approve/deny requests
- **Role Toggle** - Convert users to admins and vice versa
- **System-Wide File Access** - View, download, and delete any user's files
- **Storage Monitoring** - Track storage usage per user
- **Admin Dashboard View** - See all files from all users on dashboard

### 🎨 User Interface
- **Modern Professional Design** - Clean, contemporary UI
- **Font Awesome Icons** - Professional iconography
- **Responsive Layout** - Works on all devices
- **Real-Time Feedback** - Alert messages for all actions
- **Empty States** - Helpful messages when no content

---

## 📋 Requirements

- **Python 3.7 or higher**
- **Flask 3.0+**
- **Werkzeug 3.0+**

---

## 🚀 Installation & Setup

### 1. Download the Project

Create the following directory structure:

```
FileServer-Pro/
│
├── app.py
├── config.json (auto-generated)
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── admin.html
│
├── static/
│   └── favicon.ico (optional)
│
└── uploads/ (auto-generated)
```

### 2. Install Dependencies

Create a `requirements.txt` file:

```txt
Flask==3.0.0
Werkzeug==3.0.1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask werkzeug
```

### 3. Configure Admin Credentials

**⚠️ IMPORTANT: Before running the app for the first time!**

Open `app.py` and find these lines (around line 18-20):

```python
default_config = {
    'users': {
        'UPDATE_ADMIN_NAME': {  # ← Change this to your desired admin username
            'password': generate_password_hash('UPDATE_ADMIN_PASSWORD'),  # ← Change this to your desired password
```

**Update them with your credentials:**

```python
default_config = {
    'users': {
        'myadmin': {  # Your admin username
            'password': generate_password_hash('MySecurePassword123!'),  # Your admin password
```

### 4. Add Favicon (Optional)

1. Create a `static/` folder in your project root
2. Add your `favicon.ico` file to the `static/` folder
3. The favicon will automatically appear in browser tabs

You can generate a favicon at:
- https://favicon.io
- https://www.favicon-generator.org

### 5. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 6. First Login

1. Navigate to `http://localhost:5000`
2. Login with your configured admin credentials
3. Start managing files!

---

## 📖 User Guide

### For Regular Users

#### Registration
1. Go to `/register`
2. Fill in username, email, and password
3. Submit the request
4. Wait for admin approval

#### File Upload
1. Login to your dashboard
2. Click the upload area or drag & drop files
3. Files are uploaded instantly
4. All file types are accepted

#### File Management
1. View all your files in the dashboard table
2. Download files by clicking the "Download" button
3. Delete files by clicking the "Delete" button

### For Administrators

#### Dashboard View
- Admins see **all files from all users** on the dashboard
- Files show owner badges
- Statistics show total system storage and files
- Admin mode indicator is visible

#### User Management
1. Go to **Admin Panel** → **User Management**
2. View all users with their stats
3. **Toggle Role**: Convert users to admins or vice versa
4. **Delete User**: Remove users and all their files

#### Registration Approval
1. Go to **Admin Panel** → **Pending Requests**
2. Review registration requests
3. **Approve**: Grant user access
4. **Deny**: Reject the request

#### File Oversight
**From Dashboard:**
- View all files from all users
- Download any file
- Delete any file

**From Admin Panel:**
- See "All User Files" section
- Complete file management across the system

---

## ⚙️ Configuration

### File Upload Limits

Edit in `app.py` (line ~13):

```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
```

Change `500` to your desired limit in megabytes.

### Change Secret Key

For production, generate a new secret key:

```python
import secrets
print(secrets.token_hex(32))
```

Replace in `app.py` (line ~12):

```python
app.secret_key = 'your-generated-secret-key-here'
```

### Server Configuration

Change host and port in `app.py` (last line):

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

- `host='0.0.0.0'` - Accept connections from any IP
- `host='127.0.0.1'` - Local only
- `port=5000` - Change to any available port

---

## 🗂️ File Structure

```
FileServer-Pro/
│
├── app.py                      # Main Flask application
├── config.json                 # User database (auto-generated)
├── requirements.txt            # Python dependencies
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # User/Admin dashboard
│   └── admin.html             # Admin control panel
│
├── static/                     # Static files (optional)
│   └── favicon.ico            # Website favicon
│
└── uploads/                    # User files (auto-generated)
    ├── username1/             # User1's files
    ├── username2/             # User2's files
    └── admin/                 # Admin's files
```

---

## 🔒 Security Features

### Password Security
- ✅ Passwords hashed with Werkzeug's `generate_password_hash()`
- ✅ Never stored in plain text
- ✅ Secure comparison with `check_password_hash()`

### Session Security
- ✅ Secure session management
- ✅ Secret key for session signing
- ✅ Session-based authentication

### File Security
- ✅ File isolation per user
- ✅ Sanitized filenames with `secure_filename()`
- ✅ Permission checks on all routes
- ✅ Admin-only routes protected

### Access Control
- ✅ `@login_required` decorator
- ✅ `@admin_required` decorator
- ✅ Role-based permissions
- ✅ Protected admin account

---

## 🌐 API Endpoints

### Public Routes
- `GET /` - Home (redirects to login/dashboard)
- `GET,POST /login` - User login
- `GET,POST /register` - Registration request
- `GET /logout` - Logout

### User Routes (Authentication Required)
- `GET /dashboard` - User dashboard
- `POST /upload` - Upload file
- `GET /download/<filename>` - Download own file
- `POST /delete/<filename>` - Delete own file

### Admin Routes (Admin Only)
- `GET /admin` - Admin control panel
- `POST /admin/approve/<username>` - Approve registration
- `POST /admin/deny/<username>` - Deny registration
- `POST /admin/toggle-role/<username>` - Toggle user role
- `POST /admin/delete/<username>` - Delete user
- `GET /admin/download-file/<username>/<filename>` - Download any file
- `POST /admin/delete-file/<username>/<filename>` - Delete any file
- `POST /delete/<owner>/<filename>` - Delete user file (admin from dashboard)

---

## 🛠️ Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:** Change the port or kill the process:

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

Or change port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Config.json Error

**Error:** `JSONDecodeError: Illegal trailing comma`

**Solution:** Delete `config.json` and restart:

```bash
# Windows
del config.json

# Linux/Mac
rm config.json

# Then restart
python app.py
```

### Permission Errors

**Error:** Cannot create uploads/ or config.json

**Solution:** Ensure write permissions:

```bash
# Windows
icacls . /grant Everyone:(OI)(CI)F

# Linux/Mac
chmod 755 .
```

### Upload Fails

**Error:** File upload returns error

**Check:**
1. File size under limit (default 500MB)
2. Sufficient disk space
3. Check browser console for errors
4. Check Flask console for error messages

### Admin Panel Not Loading

**Error:** Cannot access `/admin`

**Check:**
1. Logged in as admin user
2. User role is 'admin' in config.json
3. Check Flask console for errors

### Files Not Showing

**Error:** Uploaded files don't appear

**Check:**
1. Check `uploads/<username>/` folder exists
2. Files are actually in the folder
3. Refresh the page (F5)
4. Check storage permissions

---

## 🚀 Production Deployment

### ⚠️ Important: Do NOT use Flask's development server in production!

### Using Gunicorn

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using uWSGI

1. Install uWSGI:
```bash
pip install uwsgi
```

2. Run with uWSGI:
```bash
uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app --processes 4
```

### Production Checklist

- [ ] **Change admin credentials** - Update from defaults
- [ ] **Generate new secret key** - Use `secrets.token_hex(32)`
- [ ] **Set `debug=False`** - Disable debug mode
- [ ] **Use HTTPS** - Enable SSL/TLS
- [ ] **Set up reverse proxy** - Nginx or Apache
- [ ] **Configure firewall** - Restrict access
- [ ] **Set up backups** - Backup config.json and uploads/
- [ ] **Configure file size limits** - Set appropriate limits
- [ ] **Set up logging** - Monitor application
- [ ] **Use environment variables** - For sensitive data
- [ ] **Implement rate limiting** - Prevent abuse
- [ ] **Set up monitoring** - Track performance

### Recommended Platforms

- **Heroku** - Easy deployment with buildpacks
- **DigitalOcean** - Flexible VPS hosting
- **AWS EC2** - Scalable cloud hosting
- **Railway** - Modern platform with Git integration
- **Render** - Simple deployment from Git
- **PythonAnywhere** - Python-focused hosting

### Environment Variables (Production)

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=your-admin-name
ADMIN_PASSWORD=your-admin-password
MAX_UPLOAD_SIZE=524288000
DEBUG=False
```

Update `app.py` to read from environment:

```python
import os
from dotenv import load_dotenv

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 524288000))
```

---

## 🔧 Advanced Configuration

### Custom Upload Folder

```python
app.config['UPLOAD_FOLDER'] = '/path/to/custom/uploads'
```

### Custom Config File Location

```python
CONFIG_FILE = '/path/to/custom/config.json'
```

### Enable CORS (for API usage)

```python
from flask_cors import CORS
CORS(app)
```

### Add Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
def upload_file():
    # ... existing code
```

---

## 📊 Features Comparison

| Feature | Regular User | Admin |
|---------|-------------|-------|
| Upload Files | ✅ | ✅ |
| Download Own Files | ✅ | ✅ |
| Delete Own Files | ✅ | ✅ |
| View Own Storage | ✅ | ✅ |
| View All Files | ❌ | ✅ |
| Download Any File | ❌ | ✅ |
| Delete Any File | ❌ | ✅ |
| Approve Users | ❌ | ✅ |
| Delete Users | ❌ | ✅ |
| Toggle Roles | ❌ | ✅ |
| View System Stats | ❌ | ✅ |
| Access Admin Panel | ❌ | ✅ |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🆘 Support

If you encounter any issues:

1. **Check this README** - Most common issues are covered
2. **Check Flask Console** - Error messages appear here
3. **Check Browser Console** - Frontend errors appear here
4. **Verify File Structure** - Ensure all files are in place
5. **Check Permissions** - Ensure read/write permissions
6. **Restart the Server** - Sometimes a simple restart helps

---

## 💡 Tips & Best Practices

### For Users
- Use descriptive filenames
- Regularly clean up unused files
- Check storage usage periodically
- Use strong passwords

### For Admins
- Regularly review user accounts
- Monitor storage usage
- Review pending requests promptly
- Backup config.json regularly
- Keep admin credentials secure
- Review file uploads periodically

### For Developers
- Keep dependencies updated
- Use environment variables
- Implement logging
- Add input validation
- Use HTTPS in production
- Implement rate limiting
- Add monitoring tools
- Regular security audits

---

## 🌟 Acknowledgments

Built with:
- **Flask** - Web framework
- **Werkzeug** - WSGI utilities
- **Font Awesome** - Icons
- **Python** - Programming language

---

**Made with ❤️ using Flask**

*Open your network. Share with control.*