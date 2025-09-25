"""
أداة تحميل البيانات الأساسية لخدمة البانرات - مشروع نائبك
"""
from app.models import (
    db, BannerType, BannerPosition, Banner, BannerSchedule, 
    BannerStats, UserBanner, PageBanner, BannerPermission, BannerSettings
)
from app.data.initial_data import (
    BANNER_TYPES, BANNER_POSITIONS, PAGE_BANNERS, USER_BANNERS,
    BANNER_PERMISSIONS, SAMPLE_BANNERS, BANNER_SETTINGS, BANNER_STATS
)
from datetime import datetime, timedelta
import logging

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_banner_types():
    """تحميل أنواع البانرات"""
    logger.info("تحميل أنواع البانرات...")
    
    for type_data in BANNER_TYPES:
        existing = BannerType.query.filter_by(name=type_data['name']).first()
        if not existing:
            banner_type = BannerType(**type_data)
            db.session.add(banner_type)
            logger.info(f"تم إضافة نوع البانر: {type_data['name']}")
    
    db.session.commit()
    logger.info(f"تم تحميل {len(BANNER_TYPES)} نوع بانر")


def load_banner_positions():
    """تحميل مواضع البانرات"""
    logger.info("تحميل مواضع البانرات...")
    
    for position_data in BANNER_POSITIONS:
        existing = BannerPosition.query.filter_by(name=position_data['name']).first()
        if not existing:
            position = BannerPosition(**position_data)
            db.session.add(position)
            logger.info(f"تم إضافة موضع البانر: {position_data['name']}")
    
    db.session.commit()
    logger.info(f"تم تحميل {len(BANNER_POSITIONS)} موضع بانر")


def load_page_banners():
    """تحميل بانرات الصفحات"""
    logger.info("تحميل بانرات الصفحات...")
    
    for banner_data in PAGE_BANNERS:
        existing = PageBanner.query.filter_by(page_key=banner_data['page_key']).first()
        if not existing:
            page_banner = PageBanner(**banner_data)
            page_banner.created_by = 1  # المدير الافتراضي
            page_banner.published_at = datetime.utcnow()
            db.session.add(page_banner)
            logger.info(f"تم إضافة بانر الصفحة: {banner_data['page_key']}")
    
    db.session.commit()
    logger.info(f"تم تحميل {len(PAGE_BANNERS)} بانر صفحة")


def load_user_banners():
    """تحميل بانرات المستخدمين"""
    logger.info("تحميل بانرات المستخدمين...")
    
    for banner_data in USER_BANNERS:
        existing = UserBanner.query.filter_by(
            user_id=banner_data['user_id'],
            user_type=banner_data['user_type']
        ).first()
        
        if not existing:
            user_banner = UserBanner(**banner_data)
            if banner_data.get('is_approved'):
                user_banner.approved_by = 1  # المدير الافتراضي
                user_banner.approved_at = datetime.utcnow()
            db.session.add(user_banner)
            logger.info(f"تم إضافة بانر المستخدم: {banner_data['user_id']}")
    
    db.session.commit()
    logger.info(f"تم تحميل {len(USER_BANNERS)} بانر مستخدم")


def load_banner_permissions():
    """تحميل صلاحيات البانرات"""
    logger.info("تحميل صلاحيات البانرات...")
    
    for perm_data in BANNER_PERMISSIONS:
        existing = BannerPermission.query.filter_by(
            user_id=perm_data['user_id'],
            user_type=perm_data['user_type']
        ).first()
        
        if not existing:
            permission = BannerPermission(**perm_data)
            db.session.add(permission)
            logger.info(f"تم إضافة صلاحيات: {perm_data['user_id']}-{perm_data['user_type']}")
    
    db.session.commit()
    logger.info(f"تم تحميل {len(BANNER_PERMISSIONS)} صلاحية")


def load_sample_banners():
    """تحميل البانرات التجريبية"""
    logger.info("تحميل البانرات التجريبية...")
    
    for banner_data in SAMPLE_BANNERS:
        existing = Banner.query.filter_by(title=banner_data['title']).first()
        if not existing:
            banner = Banner(**banner_data)
            banner.start_date = datetime.utcnow()
            banner.end_date = datetime.utcnow() + timedelta(days=30)
            banner.published_at = datetime.utcnow()
            db.session.add(banner)
            logger.info(f"تم إضافة البانر: {banner_data['title']}")
    
    db.session.commit()
    logger.info(f"تم تحميل {len(SAMPLE_BANNERS)} بانر تجريبي")


def load_banner_settings():
    """تحميل إعدادات النظام"""
    logger.info("تحميل إعدادات النظام...")
    
    for setting_data in BANNER_SETTINGS:
        existing = BannerSettings.query.filter_by(
            setting_key=setting_data['setting_key']
        ).first()
        
        if not existing:
            setting = BannerSettings(**setting_data)
            db.session.add(setting)
            logger.info(f"تم إضافة الإعداد: {setting_data['setting_key']}")
    
    db.session.commit()
    logger.info(f"تم تحميل {len(BANNER_SETTINGS)} إعداد")


def load_banner_stats():
    """تحميل الإحصائيات التجريبية"""
    logger.info("تحميل الإحصائيات التجريبية...")
    
    for stat_data in BANNER_STATS:
        existing = BannerStats.query.filter_by(
            banner_id=stat_data['banner_id'],
            date=stat_data['date']
        ).first()
        
        if not existing:
            stat = BannerStats(**stat_data)
            db.session.add(stat)
    
    db.session.commit()
    logger.info(f"تم تحميل {len(BANNER_STATS)} إحصائية")


def create_sample_schedules():
    """إنشاء جداول تجريبية للبانرات"""
    logger.info("إنشاء جداول البانرات التجريبية...")
    
    # جدولة البانر الأول (أيام العمل فقط)
    schedule1 = BannerSchedule(
        banner_id=1,
        days_of_week='1,2,3,4,5',  # الاثنين إلى الجمعة
        start_time=datetime.strptime('08:00', '%H:%M').time(),
        end_time=datetime.strptime('18:00', '%H:%M').time(),
        timezone='Africa/Cairo'
    )
    
    # جدولة البانر الثاني (عطلة نهاية الأسبوع)
    schedule2 = BannerSchedule(
        banner_id=2,
        days_of_week='0,6',  # الأحد والسبت
        start_time=datetime.strptime('10:00', '%H:%M').time(),
        end_time=datetime.strptime('22:00', '%H:%M').time(),
        timezone='Africa/Cairo'
    )
    
    db.session.add(schedule1)
    db.session.add(schedule2)
    db.session.commit()
    
    logger.info("تم إنشاء 2 جدول تجريبي للبانرات")


def load_all_data():
    """تحميل جميع البيانات الأساسية"""
    logger.info("بدء تحميل جميع البيانات الأساسية لخدمة البانرات...")
    
    try:
        # إنشاء الجداول
        db.create_all()
        logger.info("تم إنشاء جداول قاعدة البيانات")
        
        # تحميل البيانات بالترتيب الصحيح
        load_banner_types()
        load_banner_positions()
        load_page_banners()
        load_user_banners()
        load_banner_permissions()
        load_sample_banners()
        load_banner_settings()
        load_banner_stats()
        create_sample_schedules()
        
        logger.info("✅ تم تحميل جميع البيانات الأساسية بنجاح!")
        
        # إحصائيات نهائية
        stats = {
            'banner_types': BannerType.query.count(),
            'banner_positions': BannerPosition.query.count(),
            'page_banners': PageBanner.query.count(),
            'user_banners': UserBanner.query.count(),
            'banner_permissions': BannerPermission.query.count(),
            'sample_banners': Banner.query.count(),
            'banner_settings': BannerSettings.query.count(),
            'banner_stats': BannerStats.query.count(),
            'banner_schedules': BannerSchedule.query.count()
        }
        
        logger.info("📊 إحصائيات البيانات المحملة:")
        for key, value in stats.items():
            logger.info(f"  - {key}: {value}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحميل البيانات: {str(e)}")
        db.session.rollback()
        return False


def reset_database():
    """إعادة تعيين قاعدة البيانات"""
    logger.warning("⚠️ إعادة تعيين قاعدة البيانات...")
    
    try:
        db.drop_all()
        db.create_all()
        logger.info("✅ تم إعادة تعيين قاعدة البيانات بنجاح")
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في إعادة تعيين قاعدة البيانات: {str(e)}")
        return False


if __name__ == '__main__':
    # تشغيل تحميل البيانات مباشرة
    load_all_data()
