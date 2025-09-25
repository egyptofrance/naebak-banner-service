# -*- coding: utf-8 -*-
"""إعدادات خدمة إدارة البنرات"""

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class Config:
    """إعدادات التطبيق الأساسية"""
    
    # إعدادات Flask الأساسية
    SECRET_KEY = os.environ.get('SECRET_KEY', 'flask-insecure-banners-service-key')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # إعدادات الخدمة
    SERVICE_NAME = os.environ.get('SERVICE_NAME', 'naebak-banners-service')
    SERVICE_PORT = int(os.environ.get('PORT', 8009))
    SERVICE_VERSION = os.environ.get('SERVICE_VERSION', '1.0.0')
    
    # إعدادات قاعدة البيانات
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///banners.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات Redis
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/9')
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 9))
    
    # إعدادات رفع الملفات
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads/banners')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 5242880))  # 5MB
    ALLOWED_EXTENSIONS = set(os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif,webp,svg').split(','))
    
    # إعدادات Google Cloud Storage
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'naebak-banners-storage')
    GCS_PROJECT_ID = os.environ.get('GCS_PROJECT_ID', 'naebak-472518')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    
    # إعدادات البنرات
    MAX_BANNER_SIZE_MB = int(os.environ.get('MAX_BANNER_SIZE_MB', 5))
    MIN_BANNER_WIDTH = int(os.environ.get('MIN_BANNER_WIDTH', 300))
    MAX_BANNER_WIDTH = int(os.environ.get('MAX_BANNER_WIDTH', 1920))
    MIN_BANNER_HEIGHT = int(os.environ.get('MIN_BANNER_HEIGHT', 150))
    MAX_BANNER_HEIGHT = int(os.environ.get('MAX_BANNER_HEIGHT', 1080))
    IMAGE_OPTIMIZATION = os.environ.get('IMAGE_OPTIMIZATION', 'true').lower() == 'true'
    AUTO_RESIZE = os.environ.get('AUTO_RESIZE', 'true').lower() == 'true'
    QUALITY_COMPRESSION = int(os.environ.get('QUALITY_COMPRESSION', 85))
    
    # إعدادات CDN
    CDN_ENABLED = os.environ.get('CDN_ENABLED', 'true').lower() == 'true'
    CDN_BASE_URL = os.environ.get('CDN_BASE_URL', 'https://cdn.naebak.com/banners/')
    CACHE_DURATION = int(os.environ.get('CACHE_DURATION', 3600))
    
    # إعدادات الجدولة
    BANNER_SCHEDULING_ENABLED = os.environ.get('BANNER_SCHEDULING_ENABLED', 'true').lower() == 'true'
    AUTO_EXPIRE_BANNERS = os.environ.get('AUTO_EXPIRE_BANNERS', 'true').lower() == 'true'
    DEFAULT_BANNER_DURATION_DAYS = int(os.environ.get('DEFAULT_BANNER_DURATION_DAYS', 30))
    
    # إعدادات الأمان
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost:3000').split(',')
    MAX_BANNERS_PER_USER = int(os.environ.get('MAX_BANNERS_PER_USER', 10))
    REQUIRE_ADMIN_APPROVAL = os.environ.get('REQUIRE_ADMIN_APPROVAL', 'true').lower() == 'true'
    
    # إعدادات التسجيل
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'banners_service.log')
    
    # إعدادات المراقبة
    MONITORING_ENABLED = os.environ.get('MONITORING_ENABLED', 'false').lower() == 'true'
    HEALTH_CHECK_INTERVAL = int(os.environ.get('HEALTH_CHECK_INTERVAL', 60))
    ANALYTICS_TRACKING = os.environ.get('ANALYTICS_TRACKING', 'true').lower() == 'true'
    
    # إعدادات الخدمات الأخرى
    AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://localhost:8001')
    ADMIN_SERVICE_URL = os.environ.get('ADMIN_SERVICE_URL', 'http://localhost:8002')
    STATISTICS_SERVICE_URL = os.environ.get('STATISTICS_SERVICE_URL', 'http://localhost:8012')

class DevelopmentConfig(Config):
    """إعدادات بيئة التطوير"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    REQUIRE_ADMIN_APPROVAL = False

class ProductionConfig(Config):
    """إعدادات بيئة الإنتاج"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    MONITORING_ENABLED = True
    REQUIRE_ADMIN_APPROVAL = True

class TestingConfig(Config):
    """إعدادات بيئة الاختبار"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    BANNER_SCHEDULING_ENABLED = False
    AUTO_EXPIRE_BANNERS = False

# تحديد الإعدادات حسب البيئة
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """الحصول على إعدادات البيئة الحالية"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default'])
