"""
خدمة البانرات - مشروع نائبك
Flask + SQLite Application
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_compress import Compress
import os
import logging
from datetime import datetime
import sqlite3

# استيراد التكوين والنماذج
from config_updated import get_config, SERVICE_INFO, API_SETTINGS
from app.models import db
from app.utils.load_data import load_all_data

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """إنشاء تطبيق Flask"""
    app = Flask(__name__)
    
    # تحميل التكوين
    if config_name:
        app.config.from_object(config_name)
    else:
        config_class = get_config()
        app.config.from_object(config_class)
    
    # إنشاء مجلدات الرفع
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads/banners'), exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # تهيئة الإضافات
    db.init_app(app)
    
    # CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Rate Limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=[app.config.get('RATELIMIT_DEFAULT', '100 per hour')]
    )
    
    # Caching
    cache = Cache(app)
    
    # Compression
    Compress(app)
    
    # تسجيل الإضافات في التطبيق
    app.limiter = limiter
    app.cache = cache
    
    # إنشاء الجداول وتحميل البيانات
    with app.app_context():
        try:
            db.create_all()
            logger.info("تم إنشاء جداول قاعدة البيانات")
            
            # تحميل البيانات الأساسية إذا كانت قاعدة البيانات فارغة
            from app.models.models import BannerType
            if BannerType.query.count() == 0:
                logger.info("تحميل البيانات الأساسية...")
                load_all_data()
                
        except Exception as e:
            logger.error(f"خطأ في إنشاء قاعدة البيانات: {str(e)}")
    
    # تسجيل المسارات
    register_routes(app)
    
    logger.info(f"تم تشغيل {SERVICE_INFO['name']} v{SERVICE_INFO['version']}")
    return app


def register_routes(app):
    """تسجيل المسارات الأساسية"""
    
    @app.route('/')
    def index():
        """الصفحة الرئيسية"""
        return jsonify({
            'service': SERVICE_INFO['name'],
            'version': SERVICE_INFO['version'],
            'description': SERVICE_INFO['description'],
            'status': 'running',
            'timestamp': datetime.utcnow().isoformat(),
            'endpoints': {
                'health': '/health',
                'ready': '/ready',
                'api': API_SETTINGS['PREFIX'],
                'docs': '/api/docs'
            }
        })
    
    @app.route('/health')
    def health_check():
        """فحص صحة الخدمة"""
        try:
            # فحص قاعدة البيانات
            db.session.execute('SELECT 1')
            db_status = 'healthy'
        except Exception as e:
            db_status = f'unhealthy: {str(e)}'
        
        # فحص Redis (إذا كان مفعلاً)
        redis_status = 'not_configured'
        try:
            if hasattr(app, 'cache') and app.cache:
                app.cache.set('health_check', 'ok', timeout=1)
                if app.cache.get('health_check') == 'ok':
                    redis_status = 'healthy'
                else:
                    redis_status = 'unhealthy'
        except Exception as e:
            redis_status = f'unhealthy: {str(e)}'
        
        health_data = {
            'service': SERVICE_INFO['name'],
            'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'database': db_status,
                'cache': redis_status
            },
            'uptime': 'N/A'  # يمكن إضافة حساب الـ uptime لاحقاً
        }
        
        status_code = 200 if health_data['status'] == 'healthy' else 503
        return jsonify(health_data), status_code
    
    @app.route('/ready')
    def readiness_check():
        """فحص جاهزية الخدمة"""
        try:
            # فحص وجود البيانات الأساسية
            from app.models.models import BannerType, BannerPosition
            
            types_count = BannerType.query.count()
            positions_count = BannerPosition.query.count()
            
            if types_count > 0 and positions_count > 0:
                status = 'ready'
                message = 'Service is ready to handle requests'
            else:
                status = 'not_ready'
                message = 'Initial data not loaded'
            
            return jsonify({
                'service': SERVICE_INFO['name'],
                'status': status,
                'message': message,
                'timestamp': datetime.utcnow().isoformat(),
                'data_status': {
                    'banner_types': types_count,
                    'banner_positions': positions_count
                }
            }), 200 if status == 'ready' else 503
            
        except Exception as e:
            return jsonify({
                'service': SERVICE_INFO['name'],
                'status': 'not_ready',
                'message': f'Error checking readiness: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 503
    
    @app.route('/api/v1/banners/current')
    @app.limiter.limit("50 per minute")
    @app.cache.cached(timeout=300)  # 5 دقائق
    def get_current_banners():
        """الحصول على البانرات النشطة حالياً"""
        try:
            from app.models.models import Banner
            
            # البحث عن البانرات النشطة
            current_banners = Banner.query.filter(
                Banner.is_active == True,
                Banner.is_published == True
            ).order_by(Banner.priority.asc()).limit(5).all()
            
            # تحويل إلى JSON
            banners_data = []
            for banner in current_banners:
                if banner.is_active_now():
                    banner.increment_view_count()
                    banners_data.append(banner.to_dict())
            
            return jsonify({
                'success': True,
                'data': banners_data,
                'count': len(banners_data),
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"خطأ في جلب البانرات الحالية: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    @app.route('/api/v1/banners')
    @app.limiter.limit("30 per minute")
    def get_all_banners():
        """الحصول على جميع البانرات"""
        try:
            from app.models.models import Banner
            
            # معاملات البحث
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 50)
            is_active = request.args.get('is_active', type=bool)
            banner_type = request.args.get('type', type=int)
            
            # بناء الاستعلام
            query = Banner.query
            
            if is_active is not None:
                query = query.filter(Banner.is_active == is_active)
            
            if banner_type:
                query = query.filter(Banner.type_id == banner_type)
            
            # ترتيب وتقسيم الصفحات
            banners = query.order_by(
                Banner.priority.asc(),
                Banner.created_at.desc()
            ).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return jsonify({
                'success': True,
                'data': [banner.to_dict() for banner in banners.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': banners.total,
                    'pages': banners.pages,
                    'has_next': banners.has_next,
                    'has_prev': banners.has_prev
                },
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"خطأ في جلب البانرات: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    @app.route('/api/v1/banners/user/<int:user_id>')
    @app.limiter.limit("20 per minute")
    def get_user_banner(user_id):
        """الحصول على بانر مستخدم معين"""
        try:
            from app.models.models import UserBanner
            
            user_type = request.args.get('type', 'candidate')
            
            user_banner = UserBanner.query.filter_by(
                user_id=user_id,
                user_type=user_type,
                is_active=True
            ).first()
            
            if not user_banner:
                return jsonify({
                    'success': False,
                    'error': 'Banner not found',
                    'message': f'No banner found for user {user_id}'
                }), 404
            
            return jsonify({
                'success': True,
                'data': user_banner.to_dict(),
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"خطأ في جلب بانر المستخدم: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    @app.route('/api/v1/banners/page/<page_key>')
    @app.limiter.limit("30 per minute")
    @app.cache.cached(timeout=600)  # 10 دقائق
    def get_page_banner(page_key):
        """الحصول على بانر صفحة معينة"""
        try:
            from app.models.models import PageBanner
            
            page_banner = PageBanner.query.filter_by(
                page_key=page_key,
                is_active=True,
                is_published=True
            ).first()
            
            if not page_banner:
                return jsonify({
                    'success': False,
                    'error': 'Page banner not found',
                    'message': f'No banner found for page {page_key}'
                }), 404
            
            return jsonify({
                'success': True,
                'data': page_banner.to_dict(),
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"خطأ في جلب بانر الصفحة: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    @app.route('/api/v1/stats')
    @app.limiter.limit("10 per minute")
    def get_service_stats():
        """إحصائيات الخدمة"""
        try:
            from app.models.models import (
                Banner, BannerType, BannerPosition, 
                UserBanner, PageBanner, BannerStats
            )
            
            stats = {
                'banners': {
                    'total': Banner.query.count(),
                    'active': Banner.query.filter_by(is_active=True).count(),
                    'published': Banner.query.filter_by(is_published=True).count()
                },
                'user_banners': {
                    'total': UserBanner.query.count(),
                    'active': UserBanner.query.filter_by(is_active=True).count(),
                    'approved': UserBanner.query.filter_by(is_approved=True).count()
                },
                'page_banners': {
                    'total': PageBanner.query.count(),
                    'active': PageBanner.query.filter_by(is_active=True).count(),
                    'published': PageBanner.query.filter_by(is_published=True).count()
                },
                'types': BannerType.query.count(),
                'positions': BannerPosition.query.count(),
                'service_info': SERVICE_INFO
            }
            
            return jsonify({
                'success': True,
                'data': stats,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"خطأ في جلب الإحصائيات: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded',
            'message': str(e.description)
        }), 429


# إنشاء التطبيق
app = create_app()

if __name__ == '__main__':
    # تشغيل التطبيق
    port = int(os.environ.get('PORT', 5003))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"تشغيل خدمة البانرات على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
