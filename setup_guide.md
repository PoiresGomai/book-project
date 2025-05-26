# Django Book Management System - Setup Guide

## Complete Setup Instructions for New Environment

### Prerequisites

#### 1. Required Software
- **Python 3.8+** (Recommended: Python 3.9 or 3.10)
- **MySQL Server 5.7+** or **MySQL 8.0+**
- **Git** (for version control)

#### 2. System-Specific Requirements

**Windows:**
- Microsoft Visual C++ 14.0+ (for mysqlclient compilation)
- Or Visual Studio Build Tools

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

**macOS:**
```bash
brew install mysql pkg-config
```

### Installation Steps

#### Step 1: Environment Setup
```bash
# Clone the project (if from Git)
git clone [repository-url]
cd book_Project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# If mysqlclient fails, try:
pip install PyMySQL
```

#### Step 3: MySQL Database Setup
```sql
-- Login to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE db_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (recommended)
CREATE USER 'bookuser'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON db_book.* TO 'bookuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Step 4: Import Database
```bash
# Import the provided SQL file
mysql -u root -p db_book < db_book.sql
```

#### Step 5: Configure Django Settings
Edit `book_Project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_book',
        'USER': 'root',  # or 'bookuser'
        'PASSWORD': 'your_mysql_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

#### Step 6: Run Django
```bash
# Test database connection
python manage.py check

# Run migrations (if needed)
python manage.py migrate

# Start development server
python manage.py runserver
```

#### Step 7: Access Application
- Open browser: http://127.0.0.1:8000/manager/login
- Login credentials: `bhml` / `123456`

### Common Issues & Solutions

#### Issue 1: mysqlclient won't install
**Solution:**
```bash
pip uninstall mysqlclient
pip install PyMySQL
```

Then add to `book_Project/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

#### Issue 2: MySQL connection refused
**Solutions:**
- Ensure MySQL service is running
- Check username/password in settings.py
- Verify MySQL is listening on port 3306

#### Issue 3: Permission denied errors
**Solution:**
```bash
# Linux/Mac - fix permissions
chmod +x manage.py
```

### Development Environment Variables

Create `.env` file (optional):
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=db_book
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Production Considerations

1. **Security:**
   - Change SECRET_KEY
   - Set DEBUG=False
   - Use environment variables for sensitive data
   - Implement proper password hashing for managers

2. **Database:**
   - Use dedicated database user
   - Regular backups
   - Proper indexing

3. **Static Files:**
   - Configure static file serving
   - Use CDN for production
