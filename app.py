# -*- coding: utf-8 -*-
"""خدمة إدارة البنرات - Naebak Banners Service"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import logging
from functools import wraps

from config import get_config
from models import BannerService, BannerData, BannerStats
import constants

# إنشاء تطبيق Flask
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# إعداد CORS
CORS(app, origins=app.config['CORS_ALLOWED_ORIGINS'])

# إعداد Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per hour"]
)

# إعداد Logging
logging.basicConfig(
    level=getattr(logging, app.config['LOG_LEVEL']),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# إنشاء خدمة البنرات
banner_service = BannerService(app.config)

# إنشاء مجلد الرفع إذا لم يكن موجوداً
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def require_auth(f):
    """Decorator للتحقق من المصادقة"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "رمز المصادقة مطلوب"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    """فحص صحة الخدمة"""
    return jsonify({
        "status": "ok",
        "service": "naebak-banners-service",
        "version": app.config['SERVICE_VERSION'],
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/banners/', methods=['GET'])
@limiter.limit("50 per minute")
def get_banners():
    """الحصول على قائمة البنرات"""
    try:
        # الحصول على المعاملات
        position = request.args.get('position')
        category = request.args.get('category')
        governorate = request.args.get('governorate')
        status = request.args.get('status', 'active')
        
        # الحصول على البنرات
        banners = banner_service.get_active_banners(
            position=position,
            category=category,
            governorate=governorate
        )
        
        # تحويل إلى قواميس
        banners_data = [banner.to_dict() for banner in banners]
        
        return jsonify({
            "banners": banners_data,
            "total": len(banners_data),
            "filters": {
                "position": position,
                "category": category,
                "governorate": governorate,
                "status": status
            }
        }), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على البنرات: {str(e)}")
        return jsonify({"error": "خطأ في الحصول على البنرات"}), 500

@app.route('/api/banners/<int:banner_id>', methods=['GET'])
@limiter.limit("100 per minute")
def get_banner(banner_id):
    """الحصول على بنر محدد"""
    try:
        # بيانات تجريبية
        banner = BannerData(
            id=banner_id,
            title="بنر تجريبي",
            description="وصف البنر التجريبي",
            image_url=f"/static/banners/banner_{banner_id}.jpg",
            banner_type="hero",
            position="top",
            category="informational",
            status="active"
        )
        
        return jsonify(banner.to_dict()), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على البنر {banner_id}: {str(e)}")
        return jsonify({"error": "البنر غير موجود"}), 404

@app.route('/api/banners/', methods=['POST'])
@require_auth
@limiter.limit("10 per minute")
def create_banner():
    """إنشاء بنر جديد"""
    try:
        # التحقق من وجود ملف
        if 'image' not in request.files:
            return jsonify({"error": "ملف الصورة مطلوب"}), 400
        
        file = request.files['image']
        
        # التحقق من صحة الملف
        file_errors = banner_service.validate_image_file(file)
        if file_errors:
            return jsonify({"errors": file_errors}), 400
        
        # الحصول على بيانات البنر
        banner_data = BannerData(
            title=request.form.get('title', ''),
            description=request.form.get('description', ''),
            link_url=request.form.get('link_url', ''),
            alt_text=request.form.get('alt_text', ''),
            banner_type=request.form.get('banner_type', 'hero'),
            position=request.form.get('position', 'top'),
            category=request.form.get('category', 'informational'),
            priority=int(request.form.get('priority', 3)),
            governorate=request.form.get('governorate'),
            created_at=datetime.now()
        )
        
        # التحقق من صحة البيانات
        validation_errors = banner_service.validate_banner_data(banner_data)
        if validation_errors:
            return jsonify({"errors": validation_errors}), 400
        
        # معالجة الصورة
        image_info = banner_service.process_image(file, banner_data.banner_type)
        
        # حفظ الملف
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # تحديث رابط الصورة
        banner_data.image_url = f"/uploads/banners/{filename}"
        
        # في التطبيق الفعلي، سيتم حفظ البيانات في قاعدة البيانات
        banner_data.id = 123  # ID تجريبي
        
        return jsonify({
            "message": "تم إنشاء البنر بنجاح",
            "banner": banner_data.to_dict(),
            "image_info": image_info.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء البنر: {str(e)}")
        return jsonify({"error": "خطأ في إنشاء البنر"}), 500

@app.route('/api/banners/<int:banner_id>/click', methods=['POST'])
@limiter.limit("100 per minute")
def track_banner_click(banner_id):
    """تتبع نقرات البنر"""
    try:
        # تسجيل النقرة
        click_data = {
            "banner_id": banner_id,
            "timestamp": datetime.now().isoformat(),
            "user_agent": request.headers.get('User-Agent', ''),
            "ip_address": request.remote_addr,
            "referrer": request.headers.get('Referer', '')
        }
        
        # في التطبيق الفعلي، سيتم حفظ البيانات في قاعدة البيانات
        logger.info(f"تم تسجيل نقرة على البنر {banner_id}")
        
        return jsonify({
            "message": "تم تسجيل النقرة بنجاح",
            "banner_id": banner_id
        }), 200
        
    except Exception as e:
        logger.error(f"خطأ في تتبع النقرة: {str(e)}")
        return jsonify({"error": "خطأ في تسجيل النقرة"}), 500

@app.route('/api/banners/<int:banner_id>/stats', methods=['GET'])
@require_auth
@limiter.limit("30 per minute")
def get_banner_stats(banner_id):
    """الحصول على إحصائيات البنر"""
    try:
        stats = banner_service.get_banner_analytics(banner_id)
        return jsonify(stats.to_dict()), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على الإحصائيات: {str(e)}")
        return jsonify({"error": "خطأ في الحصول على الإحصائيات"}), 500

@app.route('/api/banners/types', methods=['GET'])
def get_banner_types():
    """الحصول على أنواع البنرات المتاحة"""
    return jsonify(constants.BANNER_TYPES), 200

@app.route('/api/banners/positions', methods=['GET'])
def get_banner_positions():
    """الحصول على مواضع البنرات المتاحة"""
    return jsonify(constants.BANNER_POSITIONS), 200

@app.route('/api/banners/categories', methods=['GET'])
def get_banner_categories():
    """الحصول على فئات البنرات المتاحة"""
    return jsonify(constants.BANNER_CATEGORIES), 200

@app.route('/uploads/banners/<filename>')
def uploaded_file(filename):
    """عرض الملفات المرفوعة"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/banners/recommendations', methods=['GET'])
@limiter.limit("20 per minute")
def get_banner_recommendations():
    """الحصول على توصيات البنرات"""
    try:
        user_id = request.args.get('user_id', type=int)
        position = request.args.get('position', 'top')
        
        recommendations = banner_service.get_banner_recommendations(user_id, position)
        recommendations_data = [banner.to_dict() for banner in recommendations]
        
        return jsonify({
            "recommendations": recommendations_data,
            "total": len(recommendations_data)
        }), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على التوصيات: {str(e)}")
        return jsonify({"error": "خطأ في الحصول على التوصيات"}), 500

# معالجات الأخطاء
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "الصفحة غير موجودة"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "خطأ داخلي في الخادم"}), 500

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({"error": "حجم الملف كبير جداً"}), 413

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=app.config['SERVICE_PORT'],
        debug=app.config['DEBUG']
    )
