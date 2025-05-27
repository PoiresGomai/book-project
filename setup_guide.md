# Django Book Management System - Setup Guide

## Complete Setup Instructions for New Environment

### Prerequisites

#### 1. Required Software
- **Miniconda/Anaconda** (Recommended) OR **Python 3.8+**
- **MySQL Server 8.0+** (We'll install this)
- **Git** (for version control)

### 🚀 Complete Database Implementation Setup

Since you don't have MySQL installed yet, we'll implement a complete database solution for your book management project.

#### Step 1: Install MySQL Server

**Option A: Download MySQL Community Server (Recommended)**
1. Visit [MySQL Downloads](https://dev.mysql.com/downloads/mysql/)
2. Download MySQL Community Server 8.0+ for Windows
3. Run the installer with these settings:
   - **Setup Type**: Developer Default
   - **Authentication Method**: Use Strong Password Encryption
   - **Root Password**: Create a strong password (remember this!)
   - **Windows Service**: Yes, start at system startup
   - **Port**: 3306 (default)

**Option B: Using MySQL Installer**
1. Download [MySQL Installer](https://dev.mysql.com/downloads/installer/)
2. Select "Custom" installation
3. Choose these products:
   - MySQL Server 8.0+
   - MySQL Workbench (GUI tool)
   - Connector/ODBC (optional)

#### Step 2: Verify MySQL Installation
```cmd
# Open Command Prompt as Administrator
# Check if MySQL service is running
sc query MySQL80

# Test MySQL connection
mysql -u root -p
# Enter your root password when prompted
```

#### Step 3: Create Project Database and User

**Connect to MySQL and create database:**
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database for book project
CREATE DATABASE db_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- IMPORTANT: For PyMySQL compatibility, use mysql_native_password
-- Step 1: Create the user with native password authentication
CREATE USER 'bookuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'BookProject123!';

-- Step 2: Grant privileges to the existing user
GRANT ALL PRIVILEGES ON db_book.* TO 'bookuser'@'localhost';

-- Step 3: Apply changes
FLUSH PRIVILEGES;

-- Verify database creation
SHOW DATABASES;

-- Verify user creation
SELECT User, Host FROM mysql.user WHERE User = 'bookuser';

-- Verify user privileges
SHOW GRANTS FOR 'bookuser'@'localhost';

-- Exit MySQL
EXIT;
```

**Alternative: If you prefer using root user for development:**
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE db_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- If using root, also change authentication method for compatibility
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_root_password';
FLUSH PRIVILEGES;

-- You can use root user directly (less secure but simpler for development)
-- Update your Django settings.py to use:
-- 'USER': 'root',
-- 'PASSWORD': 'your_root_password',

-- Exit MySQL
EXIT;
```

#### Step 4: Install Python Environment and Dependencies

**Using Conda (Recommended for PyMySQL):**
```bash
# Create and activate environment
conda create -n book_project python=3.9 -y
conda activate book_project

# Install Django
conda install django -c conda-forge -y

# IMPORTANT: Use PyMySQL instead of mysqlclient for better Windows compatibility
pip install PyMySQL

# Install additional dependencies
conda install pillow -y
pip install python-decouple
```

**IMPORTANT: Uninstall mysqlclient if already installed:**
```bash
# Remove problematic mysqlclient
pip uninstall mysqlclient -y
conda remove mysqlclient -y

# Install PyMySQL
pip install PyMySQL
```

#### Step 5: Configure Django Database Settings

Update your `book_Project/settings.py`:

```python
# Database configuration for the book management system with PyMySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_book',
        'USER': 'bookuser',                    # Use dedicated user
        'PASSWORD': 'BookProject123!',        # Use the password you set
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'autocommit': True,
            # PyMySQL specific options for better compatibility
            'connect_timeout': 20,
            'read_timeout': 20,
            'write_timeout': 20,
        },
    }
}

# For production, use environment variables:
# 'USER': os.environ.get('DB_USER', 'bookuser'),
# 'PASSWORD': os.environ.get('DB_PASSWORD', 'BookProject123!'),
```

#### Step 6: Import Existing Database Structure

Since you have a `db_book.sql` file with existing data, import it:

**Option 1: Use Command Prompt (Recommended for Windows)**
```cmd
# Open Command Prompt (cmd) - NOT PowerShell
# Navigate to your project directory
cd "C:\Users\Cluivert\CascadeProjects\book_Project\book_Project"

# Import the database
mysql -u bookuser -p db_book < db_book.sql

# When prompted, enter your password: BookProject123!
```

**Option 2: Use PowerShell with Get-Content**
```powershell
# In PowerShell, use this alternative syntax:
Get-Content db_book.sql | mysql -u bookuser -p db_book

# Or use the mysql command with file parameter:
mysql -u bookuser -p db_book --execute="source db_book.sql"
```

**Option 3: Use MySQL Workbench (GUI Method)**
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Go to Server → Data Import
4. Select "Import from Self-Contained File"
5. Choose your `db_book.sql` file
6. Select "db_book" as target schema
7. Click "Start Import"

**Option 4: Direct MySQL Command**
```cmd
# Connect to MySQL first
mysql -u bookuser -p

# Then inside MySQL prompt:
USE db_book;
SOURCE C:/Users/Cluivert/CascadeProjects/book_Project/book_Project/db_book.sql;
EXIT;
```

# Verify import was successful
mysql -u bookuser -p -e "USE db_book; SHOW TABLES;"

# Check if data was imported
mysql -u bookuser -p -e "USE db_book; SELECT COUNT(*) FROM book; SELECT COUNT(*) FROM author; SELECT COUNT(*) FROM publisher;"
```

#### Step 7: Test Django Database Connection

```bash
# Activate your environment
conda activate book_project  # or book_env\Scripts\activate

# Navigate to project directory
cd "C:\Users\Cluivert\CascadeProjects\book_Project\book_Project"

# Test database connection
python manage.py check --database default

# Check if models match database
python manage.py inspectdb

# Test queries (optional)
python manage.py shell
```

In Django shell, test your models:
```python
# Test your models
from manager.models import Book, Author, Publisher, Manager

# Check if data exists
print(f"Books: {Book.objects.count()}")
print(f"Authors: {Author.objects.count()}")
print(f"Publishers: {Publisher.objects.count()}")
print(f"Managers: {Manager.objects.count()}")

# Test a query
books = Book.objects.all()
for book in books:
    print(f"Book: {book.name}, Price: {book.price}")

exit()
```

#### Step 8: Handle Django Migrations

Since you're importing an existing database, you might need to handle migrations:

```bash
# Create migration files for your models
python manage.py makemigrations manager

# If the database already has tables, fake the initial migration
python manage.py migrate --fake-initial

# Or if you get conflicts, fake all migrations
python manage.py migrate --fake

# Run any new migrations
python manage.py migrate
```

#### Step 9: Create Django Superuser (Optional)

```bash
# Create a Django admin superuser
python manage.py createsuperuser
# Follow prompts to create username, email, and password
```

#### Step 10: Test Your Setup

```bash
# Start the Django development server
python manage.py runserver

# Visit in browser:
# http://127.0.0.1:8000/ - Your main application
# http://127.0.0.1:8000/admin/ - Django admin interface
```

### 📝 Manager Login Credentials

To access the login screen shown in the UI (图书管理系统), you need valid manager credentials.

#### Finding Existing Credentials

```bash
# Option 1: Query directly with MySQL
mysql -u bookuser -p db_book -e "SELECT number, password, name FROM manager;"

# Option 2: Use Django shell
python manage.py shell -c "from manager.models import Manager; print(list(Manager.objects.values('number', 'password', 'name')))"

#### Creating New Manager Account

If you need to create a new manager account, use the Django shell:

```python
# Start Django shell
python manage.py shell

# Create new manager
from manager.models import Manager
new_manager = Manager(number='admin', password='admin123', name='Administrator')
new_manager.save()
print("Created new manager:", new_manager.number, new_manager.name)
exit()
```

Then you can log in with:
- Account (账号): admin
- Password (密码): admin123

> ⚠️ **Security Note**: In a production environment, you should use Django's authentication system with proper password hashing rather than storing plain text passwords.

### 🔐 Django Admin vs Custom Manager Login

Your project has **two different admin systems**:

#### 1. Django Built-in Admin (`/admin/`)
- **URL**: `http://127.0.0.1:8000/admin/`
- **Purpose**: Django's built-in administration interface
- **Credentials**: Requires Django superuser account

**Create Django Superuser:**
```bash
# Navigate to project directory
cd "C:\Users\Cluivert\CascadeProjects\book_Project\book_Project"

# Activate your environment
conda activate book_project

# Create superuser
python manage.py createsuperuser

# Follow the prompts:
# Username: admin
# Email address: admin@example.com (or leave blank)
# Password: admin123 (or your preferred password)
# Password (again): admin123
```

**Then you can login at `/admin/` with:**
- Username: admin
- Password: admin123

#### 2. Custom Manager System (`/manager/`)
- **URL**: `http://127.0.0.1:8000/manager/`
- **Purpose**: Your custom book management system (图书管理系统)
- **Credentials**: Uses Manager model from database

**Find Manager Credentials:**
```bash
# Option 1: Query manager table directly
mysql -u bookuser -p db_book -e "SELECT number, password, name FROM manager;"

# Option 2: Using Django shell
python manage.py shell -c "from manager.models import Manager; [print(f'Account: {m.number}, Password: {m.password}, Name: {m.name}') for m in Manager.objects.all()]"
```

**Create New Manager Account (if needed):**
```python
# Start Django shell
python manage.py shell

# Create new manager
from manager.models import Manager
new_manager = Manager(number='admin', password='admin123', name='Administrator')
new_manager.save()
print("Created new manager:", new_manager.number, new_manager.name)
exit()
```

#### Key Differences:
- **Django Admin**: Full Django administration with user management, built-in features
- **Custom Manager**: Your beautifully designed book management interface
- **Different Users**: Completely separate user systems
- **Different URLs**: `/admin/` vs `/manager/`

### 🛠️ Troubleshooting URL Issues

#### Issue 0: Page not found (404) at root URL
**Error:** `Page not found (404)` when visiting `http://127.0.0.1:8000/`

**Solution:** Configure root URL pattern in `book_Project/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('manager/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager/', include('manager.urls')),
    path('', home_redirect, name='home'),  # Add this for root URL
]
```

**Alternative:** Visit the manager app directly at `http://127.0.0.1:8000/manager/`

#### Issue 1: Django Model Relationship Errors
**Error:** `Cannot find 'book_set' on Author object`

**Problem:** In your models, Author has a ManyToMany field to Book, so the relationship is accessed differently.

**Solution:** 
- For Author → Books: Use `author.book.all()` (not `book_set`)
- For Book → Authors: Use `book.author_set.all()` (reverse relationship)

**In your views, change:**
```python
# WRONG:
authors = models.Author.objects.prefetch_related('book_set').all()
books = author.book_set.all()

# CORRECT:
authors = models.Author.objects.prefetch_related('book').all()
books = author.book.all()
```

#### Issue 2: TemplateDoesNotExist errors
**Error:** `TemplateDoesNotExist at /public/publishers/`

**Solution:** Create missing template files in the correct directory structure:
```
manager/templates/public/
├── authors.html
├── publishers.html
├── books.html
├── home.html
└── author_detail.html
```
