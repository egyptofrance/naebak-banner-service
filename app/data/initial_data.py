"""
البيانات الأساسية لخدمة البانرات - مشروع نائبك
"""
from datetime import datetime, timedelta

# أنواع البانرات
BANNER_TYPES = [
    {
        'name': 'إعلان عام',
        'name_en': 'General Announcement',
        'description': 'إعلانات عامة للموقع',
        'icon': '📢',
        'color': '#007BFF',
        'priority': 1
    },
    {
        'name': 'تحديث نظام',
        'name_en': 'System Update',
        'description': 'إشعارات تحديثات النظام',
        'icon': '🔄',
        'color': '#17A2B8',
        'priority': 2
    },
    {
        'name': 'تحذير مهم',
        'name_en': 'Important Warning',
        'description': 'تحذيرات مهمة للمستخدمين',
        'icon': '⚠️',
        'color': '#FFC107',
        'priority': 1
    },
    {
        'name': 'ترحيب',
        'name_en': 'Welcome',
        'description': 'رسائل ترحيب للمستخدمين الجدد',
        'icon': '👋',
        'color': '#28A745',
        'priority': 3
    },
    {
        'name': 'عرض خاص',
        'name_en': 'Special Offer',
        'description': 'عروض وخصومات خاصة',
        'icon': '🎁',
        'color': '#DC3545',
        'priority': 2
    },
    {
        'name': 'إشعار طوارئ',
        'name_en': 'Emergency Notice',
        'description': 'إشعارات الطوارئ العاجلة',
        'icon': '🚨',
        'color': '#DC3545',
        'priority': 1
    }
]

# مواضع البانرات
BANNER_POSITIONS = [
    {
        'name': 'هيدر',
        'name_en': 'Header',
        'description': 'أعلى الصفحة في منطقة الهيدر',
        'css_class': 'banner-header',
        'max_banners': 1,
        'display_order': 1
    },
    {
        'name': 'هيرو',
        'name_en': 'Hero',
        'description': 'المنطقة الرئيسية أسفل الهيدر مباشرة',
        'css_class': 'banner-hero',
        'max_banners': 1,
        'display_order': 2
    },
    {
        'name': 'شريط جانبي',
        'name_en': 'Sidebar',
        'description': 'الشريط الجانبي للصفحة',
        'css_class': 'banner-sidebar',
        'max_banners': 3,
        'display_order': 3
    },
    {
        'name': 'فوتر',
        'name_en': 'Footer',
        'description': 'أسفل الصفحة في منطقة الفوتر',
        'css_class': 'banner-footer',
        'max_banners': 2,
        'display_order': 4
    },
    {
        'name': 'منبثق',
        'name_en': 'Popup',
        'description': 'نافذة منبثقة',
        'css_class': 'banner-popup',
        'max_banners': 1,
        'display_order': 5
    }
]

# بانرات الصفحات الأساسية
PAGE_BANNERS = [
    {
        'page_key': 'candidates',
        'page_name': 'صفحة المرشحين',
        'page_name_en': 'Candidates Page',
        'title': 'تصفح المرشحين',
        'title_en': 'Browse Candidates',
        'subtitle': 'اكتشف المرشحين في دائرتك الانتخابية',
        'subtitle_en': 'Discover candidates in your electoral district',
        'description': 'تصفح قائمة المرشحين وتعرف على برامجهم الانتخابية وإنجازاتهم',
        'description_en': 'Browse the list of candidates and learn about their electoral programs and achievements',
        'background_color': '#007BFF',
        'text_color': '#FFFFFF',
        'height': '400px',
        'alignment': 'center',
        'cta_text': 'ابحث عن مرشح',
        'cta_text_en': 'Find a Candidate',
        'cta_style': 'primary',
        'is_active': True,
        'is_published': True
    },
    {
        'page_key': 'representatives',
        'page_name': 'صفحة النواب',
        'page_name_en': 'Representatives Page',
        'title': 'تصفح النواب',
        'title_en': 'Browse Representatives',
        'subtitle': 'تواصل مع نوابك في البرلمان',
        'subtitle_en': 'Connect with your representatives in parliament',
        'description': 'تصفح قائمة النواب الحاليين وتابع أنشطتهم وإنجازاتهم البرلمانية',
        'description_en': 'Browse current representatives and follow their activities and parliamentary achievements',
        'background_color': '#28A745',
        'text_color': '#FFFFFF',
        'height': '400px',
        'alignment': 'center',
        'cta_text': 'ابحث عن نائب',
        'cta_text_en': 'Find a Representative',
        'cta_style': 'primary',
        'is_active': True,
        'is_published': True
    },
    {
        'page_key': 'home',
        'page_name': 'الصفحة الرئيسية',
        'page_name_en': 'Home Page',
        'title': 'مرحباً بك في نائبك',
        'title_en': 'Welcome to Naebak',
        'subtitle': 'جسر التواصل بين المواطن والنائب',
        'subtitle_en': 'Bridge of communication between citizen and representative',
        'description': 'منصة تفاعلية تربط المواطنين بممثليهم في البرلمان',
        'description_en': 'Interactive platform connecting citizens with their parliamentary representatives',
        'background_color': '#6F42C1',
        'text_color': '#FFFFFF',
        'height': '500px',
        'alignment': 'center',
        'cta_text': 'ابدأ التصفح',
        'cta_text_en': 'Start Browsing',
        'cta_style': 'primary',
        'is_active': True,
        'is_published': True
    }
]

# بانرات المستخدمين التجريبية
USER_BANNERS = [
    {
        'user_id': 1,
        'user_type': 'candidate',
        'title': 'أحمد محمد علي',
        'title_en': 'Ahmed Mohamed Ali',
        'description': 'مرشح عن دائرة القاهرة الأولى - برنامج انتخابي شامل للتنمية',
        'description_en': 'Candidate for Cairo First District - Comprehensive electoral program for development',
        'primary_color': '#007BFF',
        'secondary_color': '#6C757D',
        'text_color': '#FFFFFF',
        'layout_type': 'modern',
        'show_social_links': True,
        'show_contact_info': True,
        'is_active': True,
        'is_approved': True
    },
    {
        'user_id': 2,
        'user_type': 'representative',
        'title': 'د. فاطمة السيد',
        'title_en': 'Dr. Fatma El-Sayed',
        'description': 'نائب عن محافظة الجيزة - متخصصة في قضايا التعليم والصحة',
        'description_en': 'Representative of Giza Governorate - Specialist in education and health issues',
        'primary_color': '#28A745',
        'secondary_color': '#6C757D',
        'text_color': '#FFFFFF',
        'layout_type': 'standard',
        'show_social_links': True,
        'show_contact_info': True,
        'is_active': True,
        'is_approved': True
    },
    {
        'user_id': 3,
        'user_type': 'candidate',
        'title': 'محمد حسن إبراهيم',
        'title_en': 'Mohamed Hassan Ibrahim',
        'description': 'مرشح مستقل عن الإسكندرية - خبرة 15 سنة في العمل العام',
        'description_en': 'Independent candidate from Alexandria - 15 years experience in public service',
        'primary_color': '#DC3545',
        'secondary_color': '#6C757D',
        'text_color': '#FFFFFF',
        'layout_type': 'minimal',
        'show_social_links': False,
        'show_contact_info': True,
        'is_active': True,
        'is_approved': False  # في انتظار الموافقة
    }
]

# صلاحيات البانرات الافتراضية
BANNER_PERMISSIONS = [
    {
        'user_id': 1,
        'user_type': 'admin',
        'can_create_banners': True,
        'can_edit_banners': True,
        'can_delete_banners': True,
        'can_approve_banners': True,
        'can_edit_own_banner': True,
        'can_edit_user_banners': True,
        'can_approve_user_banners': True,
        'can_edit_page_banners': True,
        'can_publish_page_banners': True,
        'can_view_stats': True,
        'can_manage_settings': True,
        'max_banners': 100,
        'max_file_size': 10485760,  # 10MB
        'allowed_file_types': 'jpg,jpeg,png,gif,webp'
    },
    {
        'user_id': 2,
        'user_type': 'candidate',
        'can_create_banners': False,
        'can_edit_banners': False,
        'can_delete_banners': False,
        'can_approve_banners': False,
        'can_edit_own_banner': True,
        'can_edit_user_banners': False,
        'can_approve_user_banners': False,
        'can_edit_page_banners': False,
        'can_publish_page_banners': False,
        'can_view_stats': False,
        'can_manage_settings': False,
        'max_banners': 1,
        'max_file_size': 5242880,  # 5MB
        'allowed_file_types': 'jpg,jpeg,png'
    },
    {
        'user_id': 3,
        'user_type': 'representative',
        'can_create_banners': False,
        'can_edit_banners': False,
        'can_delete_banners': False,
        'can_approve_banners': False,
        'can_edit_own_banner': True,
        'can_edit_user_banners': False,
        'can_approve_user_banners': False,
        'can_edit_page_banners': False,
        'can_publish_page_banners': False,
        'can_view_stats': True,  # يمكن للنواب رؤية إحصائيات بانراتهم
        'can_manage_settings': False,
        'max_banners': 1,
        'max_file_size': 5242880,  # 5MB
        'allowed_file_types': 'jpg,jpeg,png'
    }
]

# البانرات العامة التجريبية
SAMPLE_BANNERS = [
    {
        'title': 'إعلان مهم: تحديث النظام',
        'title_en': 'Important Notice: System Update',
        'content': 'سيتم تحديث النظام يوم الجمعة من الساعة 2:00 إلى 4:00 صباحاً',
        'content_en': 'System will be updated on Friday from 2:00 AM to 4:00 AM',
        'type_id': 2,  # تحديث نظام
        'position_id': 1,  # هيدر
        'priority': 1,
        'is_active': True,
        'is_published': True,
        'show_close_button': True,
        'animation_type': 'slide'
    },
    {
        'title': 'مرحباً بك في منصة نائبك',
        'title_en': 'Welcome to Naebak Platform',
        'content': 'اكتشف كيف يمكنك التواصل مع نوابك ومتابعة أنشطتهم البرلمانية',
        'content_en': 'Discover how you can communicate with your representatives and follow their parliamentary activities',
        'link_url': '/about',
        'link_text': 'تعرف أكثر',
        'type_id': 4,  # ترحيب
        'position_id': 2,  # هيرو
        'priority': 2,
        'is_active': True,
        'is_published': True,
        'show_close_button': False,
        'animation_type': 'fade'
    },
    {
        'title': 'شارك في الاستطلاع',
        'title_en': 'Participate in Survey',
        'content': 'ما رأيك في أداء نوابك؟ شاركنا رأيك في الاستطلاع الشهري',
        'content_en': 'What do you think about your representatives\' performance? Share your opinion in our monthly survey',
        'link_url': '/survey',
        'link_text': 'شارك الآن',
        'type_id': 1,  # إعلان عام
        'position_id': 3,  # شريط جانبي
        'priority': 3,
        'is_active': True,
        'is_published': True,
        'show_close_button': True,
        'animation_type': 'bounce'
    }
]

# إعدادات النظام
BANNER_SETTINGS = [
    {
        'setting_key': 'max_active_banners',
        'setting_value': '5',
        'setting_type': 'integer',
        'description': 'الحد الأقصى للبانرات النشطة في نفس الوقت',
        'category': 'general'
    },
    {
        'setting_key': 'default_banner_duration',
        'setting_value': '7',
        'setting_type': 'integer',
        'description': 'مدة عرض البانر الافتراضية بالأيام',
        'category': 'general'
    },
    {
        'setting_key': 'auto_approve_user_banners',
        'setting_value': 'false',
        'setting_type': 'boolean',
        'description': 'الموافقة التلقائية على بانرات المستخدمين',
        'category': 'moderation'
    },
    {
        'setting_key': 'max_file_size_mb',
        'setting_value': '5',
        'setting_type': 'integer',
        'description': 'الحد الأقصى لحجم الملف بالميجابايت',
        'category': 'upload'
    },
    {
        'setting_key': 'allowed_image_types',
        'setting_value': '["jpg", "jpeg", "png", "gif", "webp"]',
        'setting_type': 'json',
        'description': 'أنواع الصور المسموحة',
        'category': 'upload'
    },
    {
        'setting_key': 'enable_banner_analytics',
        'setting_value': 'true',
        'setting_type': 'boolean',
        'description': 'تفعيل تحليلات البانرات',
        'category': 'analytics'
    },
    {
        'setting_key': 'cache_duration_minutes',
        'setting_value': '30',
        'setting_type': 'integer',
        'description': 'مدة التخزين المؤقت بالدقائق',
        'category': 'performance'
    },
    {
        'setting_key': 'notification_email',
        'setting_value': 'admin@naebak.com',
        'setting_type': 'string',
        'description': 'بريد إشعارات البانرات',
        'category': 'notifications'
    }
]

# إحصائيات تجريبية لآخر 7 أيام
def generate_sample_stats():
    """إنتاج إحصائيات تجريبية لآخر 7 أيام"""
    stats = []
    base_date = datetime.now().date()
    
    for banner_id in [1, 2, 3]:
        for i in range(7):
            date = base_date - timedelta(days=i)
            views = 100 + (i * 20) + (banner_id * 50)
            clicks = int(views * 0.05)  # 5% CTR
            
            stats.append({
                'banner_id': banner_id,
                'date': date,
                'views': views,
                'clicks': clicks,
                'unique_views': int(views * 0.8),
                'unique_clicks': int(clicks * 0.9),
                'ctr': round((clicks / views) * 100, 2),
                'avg_view_duration': 15.5 + (i * 2.3),
                'bounce_rate': 0.3 + (i * 0.05),
                'conversion_rate': 0.02 + (i * 0.01)
            })
    
    return stats

BANNER_STATS = generate_sample_stats()
