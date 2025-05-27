"""
Django Book Management System
Project initialization file
"""

# Using PyMySQL instead of mysqlclient for better Windows compatibility
import pymysql

# Use PyMySQL as MySQL driver
pymysql.install_as_MySQLdb()

