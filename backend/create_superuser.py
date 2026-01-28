#!/usr/bin/env python
"""Script to create a superuser for the Django application"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment.settings')
django.setup()

from django.contrib.auth.models import User

# Default credentials
username = 'admin'
password = 'admin123'
email = 'admin@example.com'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
    print("\nYou can use these credentials:")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    # Create superuser
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
    print("\nLogin credentials:")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("\n⚠️  IMPORTANT: Change this password in production!")
