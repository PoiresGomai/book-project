#!/usr/bin/env python3
"""
Django Book Management System - Requirements Checker
Run this script to verify all dependencies are properly installed
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False

def check_mysql_connection():
    """Check MySQL database connection"""
    try:
        import django
        import os
        
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_Project.settings')
        django.setup()
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ MySQL Database Connection")
        return True
    except Exception as e:
        print(f"❌ MySQL Database Connection - {str(e)}")
        return False

def main():
    print("🔍 Checking Django Book Management System Requirements...\n")
    
    all_good = True
    
    # Check Python version
    all_good &= check_python_version()
    
    print("\n📦 Checking Python Packages:")
    # Check required packages
    packages = [
        ("Django", "django"),
        ("MySQL Client", "MySQLdb"),  # This will check mysqlclient
    ]
    
    for package_name, import_name in packages:
        all_good &= check_package(package_name, import_name)
    
    # If MySQLdb fails, try PyMySQL
    if not check_package("PyMySQL Alternative", "pymysql"):
        print("   ℹ️  Consider installing PyMySQL as alternative")
    
    print("\n🗄️  Checking Database Connection:")
    all_good &= check_mysql_connection()
    
    print("\n" + "="*50)
    if all_good:
        print("🎉 All requirements satisfied! You can run the project.")
        print("\nNext steps:")
        print("1. python manage.py runserver")
        print("2. Open http://127.0.0.1:8000/manager/login")
        print("3. Login with: bhml / 123456")
    else:
        print("⚠️  Some requirements are missing. Please install them:")
        print("pip install -r requirements.txt")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
