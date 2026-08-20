import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

import shutil

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')
    
    # Detect Vercel / Serverless Environment
    IS_VERCEL = os.getenv('VERCEL') == '1' or os.getenv('VERCEL_ENV') is not None or os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None
    
    # Database - Handle both SQLite (local & Vercel /tmp) and PostgreSQL (production)
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        if IS_VERCEL:
            # On Vercel, filesystem is read-only except /tmp
            db_path = '/tmp/realestate.db'
            base_dir = os.path.abspath(os.path.dirname(__file__))
            bundled_dbs = [
                os.path.join(base_dir, 'instance', 'realestate.db'),
                os.path.join(base_dir, 'realestate.db')
            ]
            for bundled in bundled_dbs:
                if os.path.exists(bundled) and not os.path.exists(db_path):
                    try:
                        shutil.copy2(bundled, db_path)
                        print(f"Copied bundled DB from {bundled} to {db_path}")
                        break
                    except Exception as e:
                        print(f"Failed to copy DB to /tmp: {e}")
            database_url = f'sqlite:///{db_path}'
        else:
            database_url = 'sqlite:///realestate.db'
    
    # Fix for Render/Heroku postgres:// URL (SQLAlchemy requires postgresql://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # File Upload Settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg', 'pdf', 'doc', 'docx'}
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Pagination
    PROPERTIES_PER_PAGE = int(os.getenv('PROPERTIES_PER_PAGE', 9))
    ADMIN_PAGE_SIZE = int(os.getenv('ADMIN_PAGE_SIZE', 20))
    USER_PAGE_SIZE = int(os.getenv('USER_PAGE_SIZE', 12))
    
    # Admin Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)