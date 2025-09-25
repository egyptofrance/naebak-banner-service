"""
إعدادات خدمة البانرات - مشروع نائبك
Flask + SQLite Configuration
"""
import os
from datetime import timedelta

class Config:
    """الإعدادات الأساسية"""
    
    # إعدادات التطبيق
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'naebak-banner-service-secret-key-2024'
    
    # إعدادات قاعدة البيانات SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///naebak_banners.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 20
        }
    }
    
    # إعدادات Redis للتخزين المؤقت
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/3'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 1800  # 30 دقيقة
    
    # إعدادات Celery للمهام الخلفية
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Africa/Cairo'
    CELERY_ENABLE_UTC = True
    
    # إعدادات رفع الملفات
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads/banners'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # إعدادات الأمان
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # إعدادات CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    
    # إعدادات Rate Limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # إعدادات البانرات
    BANNER_SETTINGS = {
        'MAX_ACTIVE_BANNERS': int(os.environ.get('MAX_ACTIVE_BANNERS', '5')),
        'DEFAULT_BANNER_DURATION_DAYS': int(os.environ.get('DEFAULT_BANNER_DURATION_DAYS', '7')),
        'AUTO_APPROVE_USER_BANNERS': os.environ.get('AUTO_APPROVE_USER_BANNERS', 'false').lower() == 'true',
        'ENABLE_BANNER_ANALYTICS': os.environ.get('ENABLE_BANNER_ANALYTICS', 'true').lower() == 'true',
        'CACHE_DURATION_MINUTES': int(os.environ.get('CACHE_DURATION_MINUTES', '30')),
        'MAX_USER_BANNERS': int(os.environ.get('MAX_USER_BANNERS', '1')),
        'REQUIRE_ADMIN_APPROVAL': os.environ.get('REQUIRE_ADMIN_APPROVAL', 'true').lower() == 'true'
    }
    
    # إعدادات الصور
    IMAGE_SETTINGS = {
        'MAX_WIDTH': int(os.environ.get('MAX_IMAGE_WIDTH', '1920')),
        'MAX_HEIGHT': int(os.environ.get('MAX_IMAGE_HEIGHT', '1080')),
        'QUALITY': int(os.environ.get('IMAGE_QUALITY', '85')),
        'THUMBNAIL_SIZE': (300, 200),
        'OPTIMIZE': True,
        'PROGRESSIVE': True
    }
    
    # إعدادات الإشعارات
    NOTIFICATION_SETTINGS = {
        'ADMIN_EMAIL': os.environ.get('ADMIN_EMAIL', 'admin@naebak.com'),
        'SEND_APPROVAL_NOTIFICATIONS': os.environ.get('SEND_APPROVAL_NOTIFICATIONS', 'true').lower() == 'true',
        'SEND_STATS_REPORTS': os.environ.get('SEND_STATS_REPORTS', 'true').lower() == 'true'
    }
    
    # إعدادات الأداء
    PERFORMANCE_SETTINGS = {
        'ENABLE_GZIP': True,
        'COMPRESS_LEVEL': 6,
        'COMPRESS_MIN_SIZE': 500,
        'CACHE_STATIC_FILES': True,
        'STATIC_FILE_MAX_AGE': 31536000  # سنة واحدة
    }
    
    # إعدادات السجلات
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/banner_service.log')
    
    # إعدادات المراقبة
    MONITORING = {
        'ENABLE_METRICS': os.environ.get('ENABLE_METRICS', 'true').lower() == 'true',
        'METRICS_PORT': int(os.environ.get('METRICS_PORT', '9090')),
        'HEALTH_CHECK_ENDPOINT': '/health',
        'READY_CHECK_ENDPOINT': '/ready'
    }


class DevelopmentConfig(Config):
    """إعدادات التطوير"""
    DEBUG = True
    TESTING = False
    
    # قاعدة بيانات التطوير
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_naebak_banners.db'
    
    # تخزين مؤقت أقل في التطوير
    CACHE_DEFAULT_TIMEOUT = 300  # 5 دقائق
    
    # إعدادات أقل صرامة في التطوير
    BANNER_SETTINGS = Config.BANNER_SETTINGS.copy()
    BANNER_SETTINGS.update({
        'AUTO_APPROVE_USER_BANNERS': True,
        'REQUIRE_ADMIN_APPROVAL': False
    })


class ProductionConfig(Config):
    """إعدادات الإنتاج"""
    DEBUG = False
    TESTING = False
    
    # إعدادات أمان إضافية للإنتاج
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # إعدادات أداء محسنة
    SQLALCHEMY_ENGINE_OPTIONS = Config.SQLALCHEMY_ENGINE_OPTIONS.copy()
    SQLALCHEMY_ENGINE_OPTIONS.update({
        'pool_size': 10,
        'max_overflow': 20
    })
    
    # تخزين مؤقت أطول في الإنتاج
    CACHE_DEFAULT_TIMEOUT = 3600  # ساعة واحدة
    
    # Rate limiting أكثر صرامة
    RATELIMIT_DEFAULT = "50 per hour"


class TestingConfig(Config):
    """إعدادات الاختبار"""
    TESTING = True
    DEBUG = True
    
    # قاعدة بيانات في الذاكرة للاختبارات
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # تعطيل CSRF في الاختبارات
    WTF_CSRF_ENABLED = False
    
    # تعطيل Rate Limiting في الاختبارات
    RATELIMIT_ENABLED = False
    
    # إعدادات اختبار مبسطة
    BANNER_SETTINGS = {
        'MAX_ACTIVE_BANNERS': 10,
        'DEFAULT_BANNER_DURATION_DAYS': 1,
        'AUTO_APPROVE_USER_BANNERS': True,
        'ENABLE_BANNER_ANALYTICS': False,
        'CACHE_DURATION_MINUTES': 1,
        'MAX_USER_BANNERS': 5,
        'REQUIRE_ADMIN_APPROVAL': False
    }


# تحديد التكوين حسب البيئة
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """الحصول على التكوين المناسب"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])


# إعدادات إضافية للخدمة
SERVICE_INFO = {
    'name': 'naebak-banner-service',
    'version': '1.0.0',
    'description': 'خدمة إدارة البانرات والإعلانات - مشروع نائبك',
    'author': 'Naebak Team',
    'contact': 'info@naebak.com',
    'documentation': '/api/docs',
    'health_check': '/health'
}

# إعدادات API
API_SETTINGS = {
    'VERSION': 'v1',
    'PREFIX': '/api/v1',
    'TITLE': 'Naebak Banner Service API',
    'DESCRIPTION': 'API لإدارة البانرات والإعلانات في منصة نائبك',
    'CONTACT': {
        'name': 'Naebak Support',
        'email': 'support@naebak.com'
    },
    'LICENSE': {
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    }
}
