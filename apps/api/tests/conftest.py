import os

os.environ.setdefault(
    'JWT_SECRET_KEY', 'test-secret-key-must-be-32-characters'
)
os.environ.setdefault('SQL_ECHO', 'false')
