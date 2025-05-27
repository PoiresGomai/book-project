#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Creating default manager account if it doesn't exist..."
python manage.py shell -c "
from manager.models import Manager
if not Manager.objects.filter(number='admin').exists():
    Manager.objects.create(number='admin', password='admin123', name='Administrator')
    print('Created default admin account')
else:
    print('Admin account already exists')
"

echo "==> Build completed successfully!"
